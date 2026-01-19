# server.py
import os
from concurrent import futures

import grpc
from dotenv import load_dotenv

import travel_planner_pb2 as tp_pb2
import travel_planner_pb2_grpc as tp_pb2_grpc

from planner_pipeline import plan_trip_structured, plan_trip_nl

load_dotenv()  # for GEMINI_API_KEY etc.

class TravelPlannerServicer(tp_pb2_grpc.TravelPlannerServicer):
    def PlanTrip(self, request: tp_pb2.TripRequest, context) -> tp_pb2.TripPlan:
        try:
            prefs = dict(request.preferences)
            result = plan_trip_structured(
                city=request.city,
                start_date=request.start_date,
                end_date=request.end_date,
                preferences=prefs,
            )
            return self._dict_to_tripplan(result)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return tp_pb2.TripPlan()

    def PlanTripNL(self, request: tp_pb2.NLTripRequest, context) -> tp_pb2.TripPlan:
        try:
            result = plan_trip_nl(request.query)
            return self._dict_to_tripplan(result)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return tp_pb2.TripPlan()

    # -------- helper: dict -> protobuf --------
    def _dict_to_tripplan(self, d: dict) -> tp_pb2.TripPlan:
        pois_dict = d.get("pois", {}) or {}
        weather_dict = d.get("weather", {}) or {}
        itin_dict = d.get("itinerary", {}) or {}
        meta_dict = d.get("meta", {}) or {}

        # POIs
        center = pois_dict.get("center", {}) or {}
        poi_center = tp_pb2.Location(
            latitude=float(center.get("lat", 0.0)),
            longitude=float(center.get("lon", 0.0)),
        )
        poi_list = []
        for p in pois_dict.get("pois", []) or []:
            poi_list.append(
                tp_pb2.PointOfInterest(
                    name=p.get("name", ""),
                    category=p.get("category", ""),
                    latitude=float(p.get("lat", 0.0)),
                    longitude=float(p.get("lon", 0.0)),
                    description=p.get("short_desc", ""),
                )
            )
        poi_collection = tp_pb2.POICollection(
            city=pois_dict.get("city", ""),
            center=poi_center,
            pois=poi_list,
        )

        # Weather
        daily_list = []
        for w in weather_dict.get("daily", []) or []:
            daily_list.append(
                tp_pb2.WeatherDay(
                    date=w.get("date", ""),
                    summary=w.get("summary", ""),
                    max_temp=float(w.get("max_temp", 0.0)),
                    min_temp=float(w.get("min_temp", 0.0)),
                    weather_code=int(w.get("weathercode", 0)),
                )
            )
        weather = tp_pb2.WeatherForecast(
            latitude=float(weather_dict.get("lat", weather_dict.get("latitude", 0.0))),
            longitude=float(weather_dict.get("lon", weather_dict.get("longitude", 0.0))),
            daily=daily_list,
        )

        # Itinerary
        days_list = []
        for day in itin_dict.get("days", []) or []:
            days_list.append(
                tp_pb2.DayPlan(
                    date=day.get("date", ""),
                    morning=day.get("morning", ""),
                    afternoon=day.get("afternoon", ""),
                    evening=day.get("evening", ""),
                    notes=day.get("notes", ""),
                )
            )
        itinerary = tp_pb2.Itinerary(days=days_list)

        # Meta
        tools_called = []
        for t in meta_dict.get("tools_called", []) or []:
            tools_called.append(
                tp_pb2.ToolExecution(
                    tool_name=t.get("tool", ""),
                    result_summary=t.get("result", ""),
                )
            )
        errors = [str(e) for e in meta_dict.get("errors", []) or []]
        meta = tp_pb2.ExecutionMetadata(
            tools_called=tools_called,
            errors=errors,
        )

        return tp_pb2.TripPlan(
            pois=poi_collection,
            weather=weather,
            itinerary=itinerary,
            meta=meta,
        )

def serve():
    port = os.getenv("GRPC_PORT", "50051")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tp_pb2_grpc.add_TravelPlannerServicer_to_server(TravelPlannerServicer(), server)
    # NOTE: correct registration function name:
    # tp_pb2_grpc.add_TravelPlannerServicer_to_server(...)
    # adjust to your generated code’s function

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"gRPC server listening on {port}")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

# client.py
import grpc
import travel_planner_pb2 as tp_pb2
import travel_planner_pb2_grpc as tp_pb2_grpc

def test_plan_trip():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = tp_pb2_grpc.TravelPlannerStub(channel)
        req = tp_pb2.TripRequest(
            city="Addis Ababa",
            start_date="2025-12-22",
            end_date="2025-12-23",
        )
        resp = stub.PlanTrip(req)
        print("City:", resp.pois.city)
        print("POIs:", len(resp.pois.pois))
        print("Weather days:", len(resp.weather.daily))
        if resp.itinerary.days:
            print("First day:", resp.itinerary.days[0].date, resp.itinerary.days[0].morning)

def test_plan_trip_nl():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = tp_pb2_grpc.TravelPlannerStub(channel)
        req = tp_pb2.NLTripRequest(
            query="Plan a 2-day trip to Addis Ababa starting tomorrow"
        )
        resp = stub.PlanTripNL(req)
        print("City:", resp.pois.city)
        print("Days:", len(resp.itinerary.days))

if __name__ == "__main__":
    test_plan_trip()
    test_plan_trip_nl()

from rest_framework.views import APIView
from rest_framework.response import Response
from .ml_models.demand_predictor import predict_demand

class DemandPredictionAPI(APIView):
    def get(self, request):
        sample_history = [60, 70, 80, 75, 90]
        prediction = predict_demand(sample_history)
        return Response({'predicted_occupancy': round(prediction)})
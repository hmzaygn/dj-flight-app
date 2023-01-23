from rest_framework import serializers
from .models import (
    Flight,
    Passenger,
    Reservation
)


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "estimated_departure_time"
        )


class PassengerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passenger
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):

    passenger = PassengerSerializer(many=True, required=False)
    flight = serializers.StringRelatedField()
    flight_id = serializers.IntegerField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Reservation
        fields = (
            "id",
            "flight",
            "flight_id",
            "user",
            "passenger"
        )

    def create(self, validated_data):
        passender_data = validated_data.pop("passenger")
        validated_data["user_id"] = self.context["request"].user.id
        reservation = Reservation.objects.create(**validated_data)

        for passenger in passender_data:
            pas = Passenger.objects.create(**passenger)
            reservation.passenger.add(pas)
        
        reservation.save()
        return reservation


class StaffFlightSerializer(serializers.ModelSerializer):

    reservations = ReservationSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "estimated_departure_time",
            "reservations"
        )




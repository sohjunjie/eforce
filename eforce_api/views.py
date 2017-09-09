from django.db import IntegrityError
from django.shortcuts import render

from eforce_api.utils import get_request_body_param
from eforce_api.models import Crisis, CrisisAffectedLocation, CombatStrategy
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class CrisisStrategyView(APIView):

    permission_classes = (AllowAny, )

    def post(self, request, pk):
        """
        @body int cmo_crisis_id: id used by cmo to identify crisis event uniquely
        @body str detail: detail of strategy
        """

        try:
            crisis = Crisis.objects.get(cmo_crisis_id=pk)
        except ObjectDoesNotExist:
            return Response({'detail': "Unable to find crisis with cmo crisis id %s" % cmo_crisis_id},
                            status=status.HTTP_404_NOT_FOUND)

        strategy_detail = get_request_body_param(request, 'detail', None).strip()
        if not strategy_detail:
            return Response({'detail': 'crisis strategy cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

        CombatStrategy.objects.create(crisis=crisis, detail=strategy_detail)

        return Response({'data': 'success'}, status=status.HTTP_201_CREATED)


class CrisisCaseView(APIView):

    permission_classes = (AllowAny, )

    def post(self, request):
        """
        @body int cmo_crisis_id: id used by cmo to identify crisis event uniquely
        @body str title: crisis title or code name
        @body str description: crisis description
        @body str strategy: Strategy to combat the crisis
        @body int scale: scale of the crisis from 1 to 5
        @body [{'lat' : lat, 'lng' : lng},...] locations : affected location(s) of crisis
        """

        cmo_crisis_id = get_request_body_param(request, 'cmo_crisis_id', None)
        crisis_title = get_request_body_param(request, 'title', '').strip()
        crisis_desc = get_request_body_param(request, 'description', '').strip()
        crisis_scale = get_request_body_param(request, 'scale', 0)
        locations = get_request_body_param(request, 'locations', [])

        if not cmo_crisis_id:
            return Response({'detail': 'cmo crisis id cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        if not crisis_title:
            return Response({'detail': 'crisis title cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        if not crisis_desc:
            return Response({'detail': 'crisis description cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_crisis = Crisis.objects.create(cmo_crisis_id=cmo_crisis_id,
                                               title=crisis_title,
                                               description=crisis_desc,
                                               scale=crisis_scale)
        except IntegrityError:
            return Response({'detail': 'crisis of cmo crisis id %s already exist' % cmo_crisis_id}, status=status.HTTP_400_BAD_REQUEST)

        for loc in locations:
            try:
                lat, lng = loc['lat'], loc['lng']
                CrisisAffectedLocation.objects.create(crisis=new_crisis, lat=lat, lng=lng)
            except KeyError:
                pass

        return Response({'data': 'success'}, status=status.HTTP_201_CREATED)

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render

from eforce_api.utils import get_request_body_param, PermissionManager
from eforce_api.models import *
from eforce_api.serializers import CrisisSerializer, CrisisDetailSerializer, \
    CrisisUpdateSerializer, UserGroupImageSerializer, UserGroupSerializer, \
    InstructionSerializer, CombatStrategySerializer

from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class ThisUserGroupRoleView(APIView):

    def get(self, request):

        user = request.user
        usergroup = user.userprofile.usergroup

        serializer = UserGroupSerializer(usergroup)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class EFAssetsGroupListView(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserGroupSerializer

    def get_queryset(self):
        search = self.request.query_params.get('q', None)
        usergroups = UserGroup.objects.all()
        if search is not None and search is not '':
            search = search.replace(' ', '_')
            usergroups = usergroups.filter(rolename__icontains=search)

        return usergroups


class UserGroupImageUploadView(APIView):

    permission_classes = (AllowAny, )

    def put(self, request, pk):

        usergroup = UserGroup.objects.get(pk=pk)
        serializer = UserGroupImageSerializer(usergroup, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CrisisCaseUnresolvedSearchView(generics.ListAPIView):

    permission_classes = (AllowAny, )
    serializer_class = CrisisSerializer

    def get_queryset(self):
        search = self.request.query_params.get('q', None)
        crisis = Crisis.objects.filter(resolve=False)
        if search is not None and search is not '':
            crisis = crisis.filter(title__icontains=search)
        return crisis


class CrisisCaseDetailView(APIView):

    permission_classes = (AllowAny, )

    def get(self, request, pk):
        try:
            crisis = Crisis.objects.get(pk=pk)
        except DoesNotExist:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)

        serializer = CrisisDetailSerializer(crisis)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class CrisisCombatStrategyListView(generics.ListAPIView):
    queryset = CombatStrategy.objects.all()
    serializer_class = CombatStrategySerializer
    permission_classes = (AllowAny,)

    def list(self, request, pk):
        queryset = self.get_queryset().filter(crisis__id=pk)
        serializer = CombatStrategySerializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class CrisisUpdateListView(generics.ListAPIView):
    queryset = CrisisUpdate.objects.all()
    serializer_class = CrisisUpdateSerializer
    permission_classes = (AllowAny,)

    def list(self, request, pk):
        queryset = self.get_queryset().filter(for_crisis__id=pk)
        serializer = CrisisUpdateSerializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class CrisisInstructionListView(generics.ListAPIView):
    serializer_class = InstructionSerializer

    def list(self, request, pk):
        usergroup = request.user.userprofile.usergroup
        queryset = usergroup.instruction.filter(for_crisis__id=pk)
        serializer = InstructionSerializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class MarkAsReadCMOCrisisCase(APIView):
    def post(self, request, pk):
        try:
            crisis = Crisis.objects.get(pk=pk)
            crisis.has_read = True
            crisis.save()
        except ObjectDoesNotExist:
            return Response({'detail': "Unable to find crisis with id %s" % pk},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({'data': 'success'}, status=status.HTTP_200_OK)


class MarkAsReadCrisisInstruction(APIView):
    def post(self, request, pk):
        try:
            iga = InstructionGroupAssoc.objects.get(instruction__id=pk, to_group=request.user.userprofile.usergroup)
            iga.has_read = True
            iga.save()
        except ObjectDoesNotExist:
            return Response({'detail': "Unable to find instruction with id %s" % pk},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({'data': 'success'}, status=status.HTTP_200_OK)


class MarkAsReadCombatStrategy(APIView):
    def post(self, request, pk):
        try:
            cs = CombatStrategy.objects.get(pk=pk)
            cs.has_read = True
            cs.save()
        except ObjectDoesNotExist:
            return Response({'detail': "Unable to find combat strategy with id %s" % pk},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({'data': 'success'}, status=status.HTTP_200_OK)


class MarkAsReadEFAssetsUpdate(APIView):
    def post(self, request, pk):
        try:
            efupdate = CrisisUpdate.objects.get(pk=pk)
            efupdate.has_read = True
            efupdate.save()
        except ObjectDoesNotExist:
            return Response({'detail': "Unable to find crisis update with id %s" % pk},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({'data': 'success'}, status=status.HTTP_200_OK)


"""         CMO API VIEW            """


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

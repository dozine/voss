from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response

from .models import Customer
from call.models import VocRecord
from .serializers import CustomerSerializer
from call.serializers import RecordSerializer, RecordCreateSerializer

import logging
logger = logging.getLogger(__name__)

@api_view(['GET'])
def customer_check(request, phone):
    try:
        customer, _ = Customer.objects.get_or_create(phone=phone)
        customer.counts += 1
        customer.save()
        
        request.user.counts += 1
        request.user.save()

        customer_serializer = CustomerSerializer(customer)
        
        return Response(customer_serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(e)
        return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
        # return Response({
        #     'statusCode': 400,
        #     'errorCode': 400,
        #     'message': str(e),
        #     'result': None,
        #     'timestamp': timezone.now().isoformat()
        # }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_customer(request):
    serializer = CustomerSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        
        return Response(serializer.data)
    
    else:
        return Response(serializer.errors, status.HTTP_402_PAYMENT_REQUIRED)
        response = {
            'statusCode': 400,
            'errorCode': 400,
            'message': "Data is required.",
            'result': None,
            'timesstamp': timezone.now().isoformat()
        }
        return JsonResponse(response, status=400)

@api_view(['PUT'])
def update_customer(request, phone):
    try:
        customer = Customer.objects.get(phone=phone)
        serializer = CustomerSerializer(customer, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data)
        else:
            raise Exception(serializer.errors)
            # return JsonResponse({'errors': serializer.errors}, status=400)
    except Exception as e:
        logger.error(e)
        return Response(e, status.HTTP_500_INTERNAL_SERVER_ERROR)
        response = {
            'statusCode': 400,
            'errorCode': 400,
            'message': str(e),
            'result': None,
            'timesstamp': timezone.now().isoformat()
        }
        return JsonResponse(response, status=400)
        # return JsonResponse({'errors': e}, status=400)
        
        
@api_view(['GET'])
def special_list(request):
    serializer = CustomerSerializer(Customer.objects.filter(special_reg=True), many=True)

    return Response(serializer.data)

@api_view(['GET'])
def special_req_list(request):
    serializer = CustomerSerializer(Customer.objects.filter(special_req=True), many=True)

    return Response(serializer.data)

# 위험고객 요청 - 일반 사용자 기능
@api_view(['PATCH'])
def special_req(request):
    try :
        target = Customer.objects.get(phone=request.data["phone"])
        if target.special_reg:
            raise Exception("Invalid Data.")
        elif not target.special_req :
            target.special_req = True
        target.counts += 1
        target.save()

        serializer = CustomerSerializer(target)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        response = {
            'statusCode': 400,
            'errorCode': 400,
            'message': str(e),
            'result': None,
            'timesstamp': timezone.now().isoformat()
        }
        return JsonResponse(response, status=400)

# 위험고객 등록 - 관리자 기능
@api_view(['PATCH'])
def special_set(request):
    try :
        if request.user.role != "A" :
            raise PermissionDenied("Unauthorized access")
            # response = {
            #     'statusCode': 401,
            #     'errorCode': 401,
            #     'message': "Unauthorized",
            #     'result': None,
            #     'timesstamp': datetime.now().isoformat()
            # }
            # return JsonResponse(response, status=401)
        
        target = Customer.objects.get(phone=request.data["phone"])
        
        if not target.special_req or target.special_reg:
            raise ValidationError("Customer is not eligible for this operation")
        
        target.special_req = False
        target.special_reg = request.data['set']
        target.save()
        
        serializer = CustomerSerializer(target)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        response = {
            'statusCode': 400,
            'errorCode': 400,
            'message': str(e),
            'result': None,
            'timesstamp': timezone.now().isoformat()
        }
        return JsonResponse(response, status=400)

# 위험고객 해제 - 관리자 기능
@api_view(['PATCH'])
def special_del(request):
    try :
        if request.user.role != "A" :
            raise PermissionDenied("Unauthorized access")
        
        target = Customer.objects.get(phone=request.data["phone"])
        
        if target.special_req or not target.special_reg:
            raise ValidationError("Customer is not eligible for this operation")

        serializer = CustomerSerializer(target,
                                        data={"special_req": False, "counts": 0, "special_reg": False},
                                        partial=True
                                        )

        if serializer.is_valid() :
            serializer.save()

            return Response(serializer.data)
        else :
            raise Exception("Invalid Data.")
    except Customer.DoesNotExist:
        raise ValidationError("Customer is not eligible for this operation")
    except Exception as e:
        print(e)
        response = {
            'statusCode': 400,
            'errorCode': 'server',
            'message': str(e),
            'result': None,
            'timesstamp': timezone.now().isoformat()
        }
        return JsonResponse(response, status=400)



@api_view(['GET'])
def get_customer(request, phone):
    # phoneNumber로 crm cusomter id값 조회
    # CALL할때 필요
    # phone으로 Customer 객체 조회
    customer = get_object_or_404(Customer, phone=phone)

    data = {"customer_id": customer.id}

    # 딕셔너리를 Response로 반환
    return Response(data, status=200)


###################### 삭제할 코드 ###################### 
@api_view(['GET'])
def customers_list(request):
    serializer = CustomerSerializer(Customer.objects.all(), many=True)

    return Response(serializer.data)
    # return JsonResponse(serializer.data, safe=False)

# # detail    
# @api_view(['GET'])
# def customers_detail(request, phone):
#     try:
#         customer = Customer.objects.get(phone=phone)
#         serializer = CustomerSerializer(customer)

#         return Response(serializer.data)
#         # return JsonResponse(serializer.data, safe=True)
#     except Exception as e:
#         response = {
#             'statusCode': 400,
#             'errorCode': 400,
#             'message': str(e),
#             'result': None,
#             'timesstamp': datetime.now().isoformat()
#         }
#         return JsonResponse(response, status=400)
#         # return JsonResponse({'errors': e}, status=400)


###################### call api로 옮긴 코드 ###################### 
# # 전화 받자마자 실행
# # 이미 DB에 있는 전화번호면 counts += 1, 없는 번호면 새로 데이터 추가
# @api_view(['GET'])
# def customer_check(request, phone):
#     try:
#         customer = Customer.objects.get(phone=phone)
#         customer.counts += 1
#         serializer = CustomerSerializer(customer, data=request.data)

#         if serializer.is_valid():
#             serializer.save()

#             return Response(serializer.data)
#             # return JsonResponse(serializer.data)
#         else:
#             raise Exception("Invalid Data.")
#             # return JsonResponse({'errors': serializer.errors}, status=400)
#     except Customer.DoesNotExist as e:
#         serializer = CustomerSerializer(data={"phone": phone})

#         if serializer.is_valid():
#             serializer.save(phone=phone)

#             return Response(serializer.data)
#         else:
#             raise Exception("Invalid Data.")
#             # return JsonResponse({'errors': serializer.errors}, status=400)
#     except Exception as e:
#         print(e)
#         response = {
#             'statusCode': 400,
#             'errorCode': 400,
#             'message': str(e),
#             'result': None,
#             'timesstamp': datetime.now().isoformat()
#         }
#         return JsonResponse(response, status=400)
#         # return JsonResponse({'errors': e}, status=400)
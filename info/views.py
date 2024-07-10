from django.http import HttpRequest,HttpResponse,JsonResponse
from . models import Student,Teacher,ClassRoom
from django.db.models import F, Sum

# Create your views here.


def handleStudent(request):
    if request.method=='GET':
        manager=Student.objects.values()

        return JsonResponse({'students':list(manager)})
    

    if request.method=='POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        address = request.POST.get('address')
        division = request.POST.get('division')

        if name is not None or address is not None or division is not None:
            if id is not None:
                student=Student.objects.filter(id=id).first()
                if student is None:
                    return JsonResponse({
                        'message':f'student does not exists with id {id}'
                    })
            student = Student()
            student.name=name
            student.address=address
            student.division=division
            student.save()

            return JsonResponse({
                'message':'Updated successful !!!'
            })
        
        student=Student()
        student.name=name
        student.address=address
        student.division=division
        student.save()


        return JsonResponse({
            'message':'New record created successfully !!'
        })
    return JsonResponse({
        'message':'name, address and division are required '
    })


def handleTeacher(request):
    if request.method=='GET':
        manager = Teacher.objects.filter(deleted=False).select_related('class_rooms').annotate(
            classroom_benches=F('class_rooms__benches'),
                    classroom_floor=F('class_rooms__floor')
        ).values()
        return JsonResponse({'teachers':list(manager)})
    
    if request.method=='POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        restore = request.GET.get('restore')

        if name is not None and subject is not None:
            if id is not None:

                if restore is not None and bool(restore):
                    teacher = Teacher.objects.filter(deleted=True).filter(pk=id).first()

                    if teacher is None:
                        return JsonResponse({
                            'message': 'Teacher does not exist !!'
                        })
                    
                    teacher.deleted = False
                    teacher.save()

                    return JsonResponse({
                        'message': 'Teacher is restored !'
                    })

                teacher = Teacher.objects.filter(pk=id).first()

                if teacher is None:
                    return JsonResponse({
                        'message':f'teacher does not exist with id {id}'
                    })
                
                teacher.name=name
                teacher.subject=subject
                teacher.save()

                return JsonResponse({
                    'message':'Teacher updated successfully !!'
                })

            teacher = Teacher()
            teacher.name=name
            teacher.subject=subject
            teacher.save()
            
            return JsonResponse({
                'message':'Teacher is saved successfully !!'
            })


    if request.method =='DELETE':
        id = request.GET.get('id')
        if id is None:
            return JsonResponse({
                'message':'Required ID to delete'
            })     
            
        teacher=Teacher.objects.filter(id=id).first()

        if teacher is None:
            return JsonResponse({
                'message':f'Teacher does not exists with id {id}'  #f=FORMAT
            })
            
        teacher.deleted = True
        teacher.save()

        return JsonResponse({
            'message':'Teacher is deleted successfully !'
        }) 
    

def handleClassroom(request):
    if request.method=='GET':
        classRoom=ClassRoom.objects.values()

        return JsonResponse({'classRooms':list(classRoom)})
    
    if request.method=='POST':
        id = request.POST.get('id')
        benches = request.POST.get('benches')
        floor = request.POST.get('floor')

        if benches is not None and floor is not None:
            classRoom=ClassRoom.objects.filter(id=id).first()
            if id is None:
                classRoom=ClassRoom()
                classRoom.benches=benches
                classRoom.floor=floor
                classRoom.save()

                return JsonResponse({
                    'message':'Class room is saved successfully !!' 
                })
            
            classRoom=ClassRoom.objects.filter(id=id).first()

            if classRoom is not None:
                classRoom.benches=benches
                classRoom.floor=floor
                classRoom.save()

                return JsonResponse({
                    'message':'Class room is edited succesfully !!'
                })
            return JsonResponse({
                'message': f'Classroom does not exists with id {id}'
            })



def handleTeacherClassroom(request: HttpRequest, id):
    if request.method == 'POST':
        teacher = Teacher.objects.filter(id=id).first()

        if teacher is None:
            return JsonResponse({
                'message': f'Teacher does not exists with id {id}'
            })
        
        classroom_id = request.POST.get('classroom_id')

        if classroom_id is not None:
            classroom_id = int(classroom_id)
            classroom = ClassRoom.objects.filter(id=id).first()

            if classroom is not None:
                teacher.class_rooms.add(classroom)
                teacher.save()

                return JsonResponse({
                    'message': 'Classroom was added to the teacher'
                })
            else:
                return JsonResponse({
                    'message': f'Classroom dont exists with id {classroom_id}'
                })
        
        return JsonResponse({
            'message': 'classroom_id is required to assign classroom to teacher'
        })


def handleTeacherClassRoom(request: HttpRequest, id):

    if request.method=='POST':
        teacher=Teacher.objects.filter(id=id).first()

        if teacher is None:
            return JsonResponse({
                'message':'Teacher does not exist'
            })
        classroom_id =request.POST.get('classroom_id')

        if classroom_id is not None:
            classroom_id = int(classroom_id)
            classroom=ClassRoom.objects.filter(id=classroom_id).first()

            if classroom is not None:
                teacher.class_rooms.add(classroom)
                teacher.save()

                return JsonResponse({
                    'message': 'Classroom was assigned to the teacher'
                })

            return JsonResponse({
                'message':'Classroom does not exists'
            })
        else:
            return JsonResponse({
                'message':f'Classroom does not exist with id {classroom_id}'
            })
        


def handleTeacherClassRoom2(request:HttpRequest,id):

    if request.method == 'GET':
        teacher = Teacher.objects.filter(
            id=id
            ).select_related(
                'class_rooms'
                ).annotate(
                    classroom_benches=F('class_rooms__benches'),
                    classrooms=Sum('class_rooms'),
                    classroom_floor=F('class_rooms__floor')
                    ).values()
        return JsonResponse({
            'teacher': list(teacher)
        })

    if request.method=='POST':
        teacher=Teacher.objects.filter(id=id).first()

        if teacher is None:
            return JsonResponse({
                'message':'Teacher does not exists'
            })
        
        classRoom_id=request.POST.get('classRoom_id')
        if classRoom_id is not None:
            classRoom_id=int(classRoom_id)
            
            classRoom=ClassRoom.objects.filter(id=classRoom_id).first()

            if classRoom is not None:
                teacher.class_rooms.add(classRoom)
                teacher.save()

                return JsonResponse({
                    'message':'Teacher assigned in classroom'
                })
            else:
                return JsonResponse({
                    'message':'Classroom does not exist'
                })
        else:
            return JsonResponse({
                'message':'Class room id is required'
            })
            





            
            

            
        

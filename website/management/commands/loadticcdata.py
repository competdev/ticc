from django.core.management.base import BaseCommand, CommandError
from website.models import *
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Sets up TICC related data'

    def handle(self, *args, **options):

        campus1 = Campus(location='Belo Horizonte', number='I').save()
        campus2 = Campus(location='Belo Horizonte', number='II').save()
        campus3 = Campus(location='Leopoldina', number='III').save()
        campus4 = Campus(location='Araxá', number='IV').save()
        campus5 = Campus(location='Divinópolis', number='V').save()
        campus7 = Campus(location='Timóteo', number='VII').save()
        campus8 = Campus(location='Varginha', number='VIII').save()
        campus9 = Campus(location='Nepomuceno', number='IX').save()
        campus10 = Campus(location='Curvelo', number='X').save()
        campus11 = Campus(location='Contagem', number='XI').save()

        category1 = Category(name='Sumô', rules='Regra de Sumô', need_score=True, need_time=True).save()
        category2 = Category(name='Maratona de Programação', rules='Regra de Maratona de Programação', need_score=True, need_time=True).save()
        category3 = Category(name='Seguidor de Linha', rules='Regra de Seguidor de Linha', need_score=False, need_time=True).save()
        category4 = Category(name='Viagem ao Centro da Terra', rules='Regra de Viagem ao Centro da Terra', need_score=True, need_time=True).save()
        category5 = Category(name='Dança', rules='Regra de Dança', need_score=True, need_time=True).save()
        category6 = Category(name='Cabo de Guerra', rules='Regra de Cabo de Guerra', need_score=True, need_time=True).save()
        category7 = Category(name='Resgate de Alto Risco', rules='Regra de Resgate de Alto Risco', need_score=True, need_time=True).save()
        category8 = Category(name='Registro Multimidiático', rules='Registro Multimidiático', need_score=True, need_time=True).save()


        participant1 = Participant(name='Competidor 1', code=1, course="Engenharia de Computação", email='competido1@gmail.com', leader=True).save()
        participant2 = Participant(name='Competidor 2', code=2, course="Engenharia de Computação", email='competido2@gmail.com', leader=True).save()
        participant3 = Participant(name='Competidor 3', code=3, course="Engenharia de Computação", email='competido3@gmail.com', leader=True).save()
        participant4 = Participant(name='Competidor 4', code=4, course="Engenharia de Computação", email='competido4@gmail.com', leader=True).save()
        participant5 = Participant(name='Competidor 5', code=5, course="Engenharia de Computação", email='competido5@gmail.com', leader=True).save()
        participant6 = Participant(name='Competidor 6', code=6, course="Engenharia de Computação", email='competido6@gmail.com', leader=True).save()
        participant7 = Participant(name='Competidor 7', code=7, course="Engenharia de Computação", email='competido7@gmail.com', leader=True).save()
        participant8 = Participant(name='Competidor 8', code=8, course="Engenharia de Computação", email='competido8@gmail.com', leader=True).save()
        participant9 = Participant(name='Competidor 9', code=9, course="Engenharia de Computação", email='competido9@gmail.com', leader=True).save()
        participant10 = Participant(name='Competidor 10', code=10, course="Engenharia de Computação", email='competido10@gmail.com', leader=True).save()
        participant11 = Participant(name='Competidor 11', code=11, course="Engenharia de Computação", email='competido11@gmail.com', leader=True).save()
        participant12 = Participant(name='Competidor 12', code=12, course="Engenharia de Computação", email='competido12@gmail.com', leader=True).save()
        participant13 = Participant(name='Competidor 13', code=13, course="Engenharia de Computação", email='competido13@gmail.com', leader=True).save()
        participant14 = Participant(name='Competidor 14', code=14, course="Engenharia de Computação", email='competido14@gmail.com', leader=True).save()
        participant15 = Participant(name='Competidor 15', code=15, course="Engenharia de Computação", email='competido15@gmail.com', leader=True).save()
        participant16 = Participant(name='Competidor 16', code=16, course="Engenharia de Computação", email='competido16@gmail.com', leader=True).save()
        participant17 = Participant(name='Competidor 17', code=17, course="Engenharia de Computação", email='competido17@gmail.com', leader=True).save()
        participant18 = Participant(name='Competidor 18', code=18, course="Engenharia de Computação", email='competido18@gmail.com', leader=True).save()
        participant19 = Participant(name='Competidor 19', code=19, course="Engenharia de Computação", email='competido19@gmail.com', leader=True).save()
        participant20 = Participant(name='Competidor 20', code=20, course="Engenharia de Computação", email='competido20@gmail.com', leader=True).save()

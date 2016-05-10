import datetime
import bcrypt as bcrypt
from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from .models import (
    DBSession,
    Users,
    NutritionList,
    NutritionType,
    )


@view_config(route_name='home', renderer='templates/users.pt', permission='registered')
def userlist(request):
    users = DBSession.query(Users).all()
    return {'users': users}


@view_config(route_name='user', renderer='templates/edit.pt')
def user(request):
    uid = request.matchdict['uid']
    getuser = DBSession.query(Users).filter(uid).first()

    if 'form_submitted' in request.POST:
        getuser.email = request.POST['email']
        getuser.password = bcrypt.hashpw(str(request.POST['password']), bcrypt.gensalt(prefix=b"2a"))
        getuser.first_name = request.POST['firstname']
        getuser.last_name = request.POST['lastname']
        getuser.dob = request.POST['dob']
        getuser.zip_code = request.POST['zipcode']
        return HTTPFound(location='/')

    return {'user': getuser}


@view_config(route_name='newuser', renderer='templates/new.pt')
def newuser(request):
    if 'form_submitted' in request.POST:
        email = request.POST['email']
        password = bcrypt.hashpw(str(request.POST['password']), bcrypt.gensalt(prefix=b"2a"))
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        dob = datetime.datetime.strptime(request.POST['dob'], '%Y-%m-%d')
        zip_code = request.POST['zipcode']
        if DBSession.query(Users).filter(Users.email == email).first():
            request.session.flash("Email address in use.")
            return HTTPFound(location='/')
        password = bcrypt.hashpw(password, bcrypt.gensalt(prefix=b"2a"))
        adduser = Users(email=email, password=password, first_name=first_name,
                        last_name=last_name, dob=dob, zip_code=zip_code,
                        created_ts=datetime.datetime.now())
        DBSession.add(adduser)
        DBSession.flush()
        return HTTPFound(location='/')

    return {}


@view_config(route_name='deleteuser')
def deleteuser(request):
    uid = request.matchdict['uid']
    getuser = DBSession.query(Users).filter(Users.uid == uid).first()
    if getuser.email == authenticated_userid(request):
        request.session.flash("You cannot delete yourself.")
        return HTTPFound(location='/')

    DBSession.delete(getuser)
    DBSession.flush()
    request.session.flash("User Deleted.")
    return HTTPFound(location='/')









@view_config(route_name='addnutritiontype', renderer='templates/addnutritiontype.pt')
def addnutritiontype(request):
    if 'form_submitted' in request.POST:
        name = request.POST['nutritionname']
        if DBSession.query(NutritionType).filter(NutritionType.name == name).first():
            request.session.flash("NutritionType already exists")
            return HTTPFound(location='/addnutritiontype')
        addnutrition = NutritionType(name=name)
        DBSession.add(addnutrition)
        DBSession.flush()
        request.session.flash("NutritionType added sucessfully")
        return HTTPFound(location='/addnutritiontype')

    return {}


@view_config(route_name='nutritionlist', renderer='templates/nutritionlist.pt')
def nutritionlist(request):
    nutritionlist = DBSession.query(NutritionList).all()
    return {'nutritionlist': nutritionlist}

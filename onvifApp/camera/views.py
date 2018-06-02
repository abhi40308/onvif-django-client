from django.shortcuts import render
from django.views.generic.base import View
from onvif import ONVIFCamera
from django.shortcuts import redirect
from django.shortcuts import render, render_to_response
import os
from django.template import RequestContext
from onvifApp.settings import BASE_DIR
from camera.models import Camera
# import zeep
# from zeep.wsse.username import UsernameToken


# Create your views here.
class CameraView(View):

    def get(self, request, *args, **kwargs):
        
        # Get Hostname
        obj = Camera.objects.get(id=kwargs['id'])
        mycam = None
        try:
            mycam = ONVIFCamera(obj.ip, obj.port, obj.username, obj.password, '/usr/local/lib/python2.7/site-packages/wsdl/')
            resp = mycam.devicemgmt.GetHostname()
            print ('My camera`s hostname: ', str(resp.Name))
            resp_name = str(resp.Name)
            print('resp name ', resp_name)
            if resp_name == 'None':
                obj.delete()
                return render( request,
			        'camera_login.html', {'success': 'False'})
        except Exception as e:
            print('Exception message : ' , str(e))
            obj.delete()
            return render( request,
			        'camera_login.html', {'success': 'False'})
        print('mycam ; ', mycam)

        # print('mycam is : ',mycam)
        
        # request.session['mycam'] = mycam
        # return redirect(
		# 	'camera_detail', host=str(resp.Name))

        # mycam = request.session.get('mycam', None)
        # resp = mycam.devicemgmt.GetHostname()
        # print ('My camera`s hostname: ', str(resp.Name))
        # dt = mycam.devicemgmt.GetSystemDateAndTime()
        # tz = dt.TimeZone
        # year = dt.UTCDateTime.Date.Year
        # hour = dt.UTCDateTime.Time.Hour
        # print('date tz year hour', dt, tz, year, hour)
        # ptz_service = mycam.create_media_service()
        # # Get ptz configuration
        # ptz_service.GetVideoSources()
        # print('ptz viedo sources : ', ptz_service)

        return render( request,
			'camera_detail.html')

        # from zeep.wsse.username import UsernameToken
        # client = zeep.Client('https://www.onvif.org/ver10/media/wsdl/media.wsdl', wsse=UsernameToken('user', 'password', use_digest=True))
        # service = client.create_service('{http://www.onvif.org/ver10/media/wsdl}MediaBinding', 'http://127.0.0.1:80/onvif/media_service')
        # service.GetProfiles()

        # ptz_service.GetStreamUri()
        # print(ptz_service)

        #obj = mycam.create_media_service()
        #profiles = obj.GetProfiles()
        #print('profiles are : ', profiles)
        #token = profiles[0]._token
        # media_service = mycam.create_media_service()
        # profiles = media_service.GetProfiles()
        # token = profiles[0]._token
        # obj = media_service.create_type('GetStreamUri')
        # obj.ProfileToken = token
        # obj.StreamSetup.Stream = 'RTP-Unicast'
        # obj.StreamSetup.Transport.Protocol = 'RTSP'
        # print(media_service.GetStreamUri(obj))
        #print(obj)

    def post(self, request, *args, **kwargs):
        print('nothing')

class CameraLoginView(View):

    def get(self, request, *args, **kwargs):     
        return render( request,
			'camera_login.html')

    def post(self, request, *args, **kwargs):
        ip = request.POST.get('ip-add','') 
        port = request.POST.get('port', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        obj_list = None
        try:
            obj_list = Camera.objects.all()
        except:
            obj_list = None
        obj = None
        if obj_list:
            try:
                obj = Camera.objects.get(ip=ip)
            except:
                obj = None
        if obj == None:
            Camera.objects.create(ip=ip, port=port,
                username=username, password=password)
            obj = Camera.objects.get(ip=ip)
        return redirect(
			'camera_detail', obj.id)
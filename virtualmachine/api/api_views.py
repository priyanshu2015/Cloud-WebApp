from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import VirtualMachine
from rest_framework.authentication import TokenAuthentication
import os

class CreateVirtualMachine(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes =(IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        #avaiable_os = os.system("VBoxManage list ostypes")
        #print(avaiable_os)
        vm_db_record = VirtualMachine.objects.create(root_user = request.user, os="Ubuntu_64")
        vm_os = "ubuntu_os"
        vm_name = str(request.user.id) + "_" + str(vm_db_record.id) + "_" + vm_os
        create_vm_command = "VBoxManage createvm --name " + vm_name + " --ostype Ubuntu_64 --register"
        vm_resouce_allocation_command = "VBoxManage modifyvm " + vm_name + " --cpus 2 --memory 2048 --vram 12"
        vm_network_adapter_command = "VBoxManage modifyvm " + vm_name + " --nic1 bridged --bridgeadapter1 eth0"
        vm_attach_virtual_media_command = '''VBoxManage createhd --filename "C:/Users/Priyanshu Gupta/VirtualBox VMs/UbuntuServer/''' + vm_name + '''.vdi" --size 5120 --variant Standard''' 
        vm_add_storage_controller = '''VBoxManage storagectl ''' + vm_name + ''' --name "SATA Controller" --add sata --bootable on'''
        vm_attach_hd_to_controller = '''VBoxManage storageattach ''' + vm_name + ''' --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium "C:/Users/Priyanshu Gupta/VirtualBox VMs/UbuntuServer/''' + vm_name + '''.vdi"'''
        vm_install_os = '''VBoxManage storagectl ''' + vm_name + ''' --name "IDE Controller" --add ide'''
        vm_attach_iso = '''VBoxManage storageattach ''' + vm_name + ''' --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium "D:/ubuntu20.04/ubuntu-20.04.2.0-desktop-amd64.iso"'''
        vm_info_command = "VBoxManage showvminfo " + vm_name
        vm_start = "VBoxManage startvm " + vm_name
        created_vm = os.system(create_vm_command + " && " + vm_resouce_allocation_command + " && " + vm_network_adapter_command + " && " + vm_attach_virtual_media_command + " && " + vm_add_storage_controller+ " && " + vm_attach_hd_to_controller + " && " + vm_install_os + " && " + vm_attach_iso + " && " + vm_info_command + " && " + vm_start)
        print(created_vm)
        return Response({"result":["Done"]})

import sys
sys.path.append('../VREP_RemoteAPIs')
import sim as vrep_sim

# CartPole simulation model for VREP
class CartPoleSimModel():
    def __init__(self, name='CartPole'):
        """
        :param: name: string
            name of objective
        """
        super(self.__class__, self).__init__()
        self.name = name
        self.client_ID = None

        self.prismatic_joint_handle = None
        self.revolute_joint_handle = None

    def initializeSimModel(self, client_ID):
        try:
            print ('Connected to remote API server')
            client_ID != -1
        except:
            print ('Failed connecting to remote API server')

        self.client_ID = client_ID

        return_code, self.prismatic_joint_handle = vrep_sim.simxGetObjectHandle(client_ID, 'prismatic_joint', vrep_sim.simx_opmode_blocking)
        if (return_code == vrep_sim.simx_return_ok):
            print('get object prismatic joint ok.')

        return_code, self.revolute_joint_handle = vrep_sim.simxGetObjectHandle(client_ID, 'revolute_joint', vrep_sim.simx_opmode_blocking)
        if (return_code == vrep_sim.simx_return_ok):
            print('get object revolute joint ok.')

        # Get the joint position
        return_code, q = vrep_sim.simxGetJointPosition(self.client_ID, self.prismatic_joint_handle, vrep_sim.simx_opmode_streaming)
        return_code, q = vrep_sim.simxGetJointPosition(self.client_ID, self.revolute_joint_handle, vrep_sim.simx_opmode_streaming)

        # Set the initialized position for each joint
        self.setJointTorque(0)
    
    def getJointPosition(self, joint_name):
        """
        :param: joint_name: string
        """
        q = 0
        if joint_name == 'prismatic_joint':
            return_code, q = vrep_sim.simxGetJointPosition(self.client_ID, self.prismatic_joint_handle, vrep_sim.simx_opmode_buffer)
        elif joint_name == 'revolute_joint':
            return_code, q = vrep_sim.simxGetJointPosition(self.client_ID, self.revolute_joint_handle, vrep_sim.simx_opmode_buffer)
        else:
            print('Error: joint name: \' ' + joint_name + '\' can not be recognized.')

        return q

    def setJointTorque(self, torque):
        if torque >= 0:
            vrep_sim.simxSetJointTargetVelocity(self.client_ID, self.prismatic_joint_handle, 1000, vrep_sim.simx_opmode_oneshot)
        else:
            vrep_sim.simxSetJointTargetVelocity(self.client_ID, self.prismatic_joint_handle, -1000, vrep_sim.simx_opmode_oneshot)

        vrep_sim.simxSetJointMaxForce(self.client_ID, self.prismatic_joint_handle, abs(torque), vrep_sim.simx_opmode_oneshot)

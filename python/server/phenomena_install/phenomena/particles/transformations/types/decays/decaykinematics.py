from __future__ import division
import math, random
from phenomena.particles.transformations.types import KinematicsCalculations, LABNBody
from phenomena.particles.models.undercoverparticle import UndercoverParticle

class DecayKinematics(KinematicsCalculations):
    '''
    We expect initialparticle to be a LorentzVector and outputparticles a list of LorentzVectors
    '''

    def __init__(self, initialparticle, target, finalparticles):
        super(DecayKinematics, self).__init__(initialparticle, target, finalparticles)

    def _set_calculations(self):
        if len(self._final) == 2:
            calculations = LAB2BodyDecay(self._initial,self._target,self._final)
        elif len(self._final) == 3:
            calculations = LAB3BodyDecay(self._initial,self._target,self._final)
        elif len(self._final) == 4:
            calculations = LAB4BodyDecay(self._initial,self._target,self._final)
        else:
            calculations = []
        self._calculations = calculations

class LAB2BodyDecay(LABNBody):

    def __init__(self, initialparticle, target, finalparticles):
        super(LAB2BodyDecay, self).__init__(initialparticle, target, finalparticles)

    def _setInitialParticleLAB(self,initialparticle):
        self._initialparticleLAB = initialparticle

    def _setBoost(self):
        self._setBoostVector()
        self._initialparticleCM  = self._initialparticleLAB.fourMomentum.boost(self._boostVector)

    def _setBoostVector(self):
        self._boostVector = self._initialparticleLAB.fourMomentum.boostvector

    def _setS(self):
        #self._s = self._initialparticleCM.e**2
        self._s = self._initialparticleLAB.mass**2

    def _setCM(self):
        self._setS()
        self._setP(self._s,self._finalparticlesCM[0].mass,self._finalparticlesCM[1].mass)
        self._setFourMomenta()


class LAB3BodyDecay(LABNBody):

    def __init__(self,initialparticle,target,finalparticles):
        self._initialparticleLAB = initialparticle
        self._finalparticlesLAB= finalparticles
        self._final1 = finalparticles[0]
        self._final2 = finalparticles[1]
        self._final3 = finalparticles[2]
        self._setBoostVector()
        self._setDalitz()
        self._setCM()

    def _setBoostVector(self):
        self._boostVector = self._initialparticleLAB.fourMomentum.boostvector

    def _setCM(self):
        # Step 1: solve the system M -> m12 + m3 in the M CM
        self._part12 = UndercoverParticle('part12', self._m12)
        self._outputStep1= LAB2BodyDecay(self._initialparticleLAB,None,[self._part12,self._final3]).finalState
        #Step 2: solve the system m12 -> m1+m2 in the M CM
        self._outputStep2 = LAB2BodyDecay(self._outputStep1[0],None, [self._final1,self._final2]).finalState
        # 1,2,3 in the M CM in finalparticles
        self._finalparticlesLAB= [self._outputStep2[0],self._outputStep2[1],self._outputStep1[1]]

    def _setLAB(self):
        for index,item in enumerate(self._finalparticlesLAB):
            self._finalparticlesCM[index].fourMomentum=self._finalparticlesCM[index].fourMomentum.boost(-1*self._boostVector)

        self._finalparticlesLAB = self._finalparticlesCM

    def _setDalitz(self):
        M = self._initialparticleLAB.mass
        m1 = self._final1.mass
        m2 = self._final2.mass
        m3 = self._final3.mass
        m12 = random.uniform(m1+m2,M-m3)
        self._m12 = m12

    @property
    def finalState(self):
        return self._finalparticlesLAB

class LAB4BodyDecay(LABNBody):

    def __init__(self,initialparticle,target,finalparticles):
        self._initialparticleLAB = initialparticle
        self._finalparticlesLAB= finalparticles
        self._final1 = finalparticles[0]
        self._final2 = finalparticles[1]
        self._final3 = finalparticles[2]
        self._final4 = finalparticles[2]
        self._setBoostVector()
        self._setDalitz()
        self._setCM()

    def _setBoost(self):
        self._setBoostVector()

    def _setBoostVector(self):
        self._boostVector = self._initialparticleLAB.fourMomentum.boostvector

    def _setCM(self):
        # Step 1: solve the system M -> m12 + m3 in the M CM
        self._part12 = UndercoverParticle('part12', self._m12)
        self._part34 = UndercoverParticle('part34', self._m34)
        self._outputStep1_12= LAB2BodyDecay(self._initialparticleLAB,None,[self._part12,self._part34]).finalState
        self._outputStep1_34= LAB2BodyDecay(self._initialparticleLAB,None,[self._part34,self._part12]).finalState
        #Step 2: solve the system m12 -> m1+m2 in the M CM
        self._outputStep2_12 = LAB2BodyDecay(self._outputStep1_12[0],None, [self._final1,self._final2]).finalState
        self._outputStep2_34 = LAB2BodyDecay(self._outputStep1_34[0],None, [self._final3,self._final4]).finalState
        # 1,2,3 in the M CM in finalparticles
        self._finalparticlesLAB= [self._outputStep2_12[0],self._outputStep2_12[1],self._outputStep2_34[0],self._outputStep2_34[1]]

    def _setLAB(self):
        for index,item in enumerate(self._finalparticlesLAB):
            self._finalparticlesCM[index].fourMomentum=self._finalparticlesCM[index].fourMomentum.boost(-1*self._boostVector)

        self._finalparticlesLAB = self._finalparticlesCM

    def _setDalitz(self):
        M = self._initialparticleLAB.mass
        m1 = self._final1.mass
        m2 = self._final2.mass
        m3 = self._final3.mass
        m4 = self._final3.mass
        m12 = random.uniform(m1+m2,M-m3-m4)
        self._m12 = m12
        m34 = random.uniform(m3+m4,M-m1-m2)
        self._m34 = m34

    @property
    def finalState(self):
        return self._finalparticlesLAB

#ifdef DEBUG
#define DEBUG_MSG(str) do { std::cout << str << std::endl; } while( false )
#else
#define DEBUG_MSG(str) do { } while ( false )
#endif

#include "ListManager.h"
#include <mutex>



ListManager::ListManager(){
}

bool ListManager::isEmpty(){
  return particleMap.empty();
}

bool ListManager::isScreenEmpty(){
  return numberOnScreen()==0;
}


void ListManager::updateMap(PhenomenaCMD phenoCMD) {
    if (phenoCMD.getCMD() == "ADD"){
      int id = phenoCMD.getParams().parent;
      auto particleIt = particleMap.find(id);
      if (id ==-1 || particleIt != particleMap.end()){
        ofLog(OF_LOG_NOTICE, ofGetTimestampString() + " Inserting id: " + ofToString(phenoCMD.getParams().id));
        shared_ptr<ParticleData> newParticleData =
        make_shared<ParticleData>(phenoCMD.getParams().id,
                                  phenoCMD.getParams().parent,
                                  phenoCMD.getParams().name,
                                  phenoCMD.getParams().mass,
                                  phenoCMD.getParams().charge,
                                  phenoCMD.getParams().type,
                                  phenoCMD.getParams().energy,
                                  phenoCMD.getParams().symbolName
                                );

        ofPoint position;
        auto particleIt = particleMap.find(phenoCMD.getParams().parent);
        if (particleIt != particleMap.end()) {
          position.set(particleIt->second->getPosition());
        }
        else {
          position.set(ofGetWidth()/2, ofGetHeight()/2,0);
        }

        ofVec2f velocity;
        velocity.set(phenoCMD.getParams().vy,phenoCMD.getParams().vz);
        velocity.scale((float) phenoCMD.getParams().beta);
        ofLog(OF_LOG_NOTICE, ofGetTimestampString() + "Particle Name " + phenoCMD.getParams().name + " " +  ofToString(phenoCMD.getParams().beta));
        std::unique_lock<std::mutex> lck (this->_mtx);
        particleMap.insert(make_pair(phenoCMD.getParams().id, make_shared<Particle>(newParticleData,position, velocity)));
      }
    }
    else if (phenoCMD.getCMD() == "REMOVE"){
        map <int, shared_ptr<Particle>>::const_iterator i = particleMap.find(phenoCMD.getParams().id);
        if (i != particleMap.end()) {
            ofLog(OF_LOG_NOTICE, ofGetTimestampString() + "Removing id: " + ofToString(phenoCMD.getParams().id));
            std::unique_lock<std::mutex> lck (this->_mtx);
            particleMap.erase(i);
        }
        else{
            ofLog(OF_LOG_NOTICE,  ofGetTimestampString() + "The particle is not in particleMap! ");
        }
    }

    else if (phenoCMD.getCMD() == "PURGE"){
        ofLog(OF_LOG_NOTICE, ofGetTimestampString() + "Erasing all particles in particleMap! PURGE!");
        std::unique_lock<std::mutex> lck (this->_mtx);
        particleMap.clear();
    }
    ofLog(OF_LOG_NOTICE,ofGetTimestampString() +  "particleMap size is: " + ofToString(particleMap.size()));
}

void ListManager::cleanupList(){
  for(auto iter=particleMap.begin(); iter!=particleMap.end(); ){
    if (particleIsOutOfBounds(iter->second)){
      std::unique_lock<std::mutex> lck (this->_mtx);
      particleMap.erase(iter++);
    }
    else{++iter;}
  }
}

int ListManager::numberOnScreen(){
  int counter = 0;
  std::unique_lock<std::mutex> lck (this->_mtx);
  for(auto pair:particleMap) {
    if (!particleIsOutOfBounds(pair.second)){
      counter++;
    }
  }
  return counter;
}


bool ListManager::particleIsOutOfBounds(const shared_ptr<Particle>& _particle){
  bool outOfBounds = false;
  ofVec2f position = _particle->getPosition();
  if (position.x > ofGetWidth()+padding || position.x < 0-padding || position.y > ofGetHeight()+padding || position.y < 0-padding){
    outOfBounds = true;
  }
  return outOfBounds;
}


void ListManager::update(){
  std::unique_lock<std::mutex> lck (this->_mtx);
  for(auto pair:particleMap) {
    pair.second->update();
  }
  //cleanupList();
}

void ListManager::draw(){

}

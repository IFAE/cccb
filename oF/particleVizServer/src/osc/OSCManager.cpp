#ifdef DEBUG
#define DEBUG_MSG(str) do { std::cout << str << std::endl; } while( false )
#else
#define DEBUG_MSG(str) do { } while ( false )
#endif

#include "OSCManager.h"

OSCManager::OSCManager(){
}

void OSCManager::setup(int _port, shared_ptr<ListManager>& _listManager){
  listManager = _listManager;
  oscReceiver.setup(_port);
}

void OSCManager::threadedFunction(){
  while(isThreadRunning()) {
    while(oscReceiver.hasWaitingMessages()){
        ofxOscMessage message;
        oscReceiver.getNextMessage(message);
        if(message.getAddress() == "/particle/operation"){
            listManager->updateMap(oscHandler.releaseParticle(message));
        }
        else if (message.getAddress().find("/particle/attributes") != string::npos) {
            oscHandler.acumulativeParticleParse(message);
        }
        else{
        }
    }
	std::this_thread::yield();
  }
}

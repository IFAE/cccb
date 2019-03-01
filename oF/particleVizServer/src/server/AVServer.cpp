//
//  AVServer.cpp
//  oscReceiveExample
//
//  Created by Oscar Martinez Carmona on 05/02/2019.
//

#include "AVServer.hpp"

AVServer::AVServer(){}

void AVServer::begin(int port){
    oscReceiver.setup(port);
}

void AVServer::update(){
     while(oscReceiver.hasWaitingMessages()){
         ofxOscMessage message;
         oscReceiver.getNextMessage(message);
         if(message.getAddress() == "/particle/operation"){
             manageAV.update(oscHandler.releaseParticle(message));
         }
         else if (message.getAddress() != "/particle/operation") {
             oscHandler.acumulativeParticleParse(message);
         }
         else{

         }
     }
}
void AVServer::draw(){
    manageAV.draw();
}
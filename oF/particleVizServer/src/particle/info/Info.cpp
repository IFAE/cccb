#include "Info.h"

Info::Info(shared_ptr<ParticleData>& _data, float _radius): data(_data), radius(_radius){
  infoFont = FontsManager::getFont("MADBold10");
}

void Info::drawInfo(ofVec2f& _velocity){
  ofVec2f textPosition = _velocity.getNormalized().getScaled(radius);
  float deltax = 30*textPosition.getNormalized().x;
  float deltay = 30*textPosition.getNormalized().y;

  string name = this->getName();
  infoFont->drawString(name, textPosition.x+deltax, textPosition.y+deltay);
}

string Info::getName(){
  string name = data->getName();
  if (name == "h0(H_1)"){
    name = "H0";
  }
  return name;
}

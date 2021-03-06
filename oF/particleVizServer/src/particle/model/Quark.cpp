#include "Quark.h"
#include "Parameters.h"

void Quark::setXMLSettingsName(){
  xmlSettingsName = "quark";
}

void Quark::specificParameters(){
  // string name = data->getName();
  // const string quarks[] = {"u", "ubar", "d", "dbar","c","cbar","s","sbar","b","bar"};
  // auto it = find(begin(quarks), end(quarks), name);
  // if (it != end(quarks)) {radius = 10;}
  float mass = data->getMass();
  if (mass!=0){radius = baseRadius*mass;}
}

Quark::Quark(shared_ptr<ParticleData>& _particleData):Model(_particleData){
  setXMLSettingsName();
  buildParameters();
  specificParameters();
  setShape();
  setInfo();
}

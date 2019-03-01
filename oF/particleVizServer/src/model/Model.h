#ifndef _Model //
#define _Model //
#include "ofMain.h"
#include "WaveRingVariation.h"
#include "ParticleData.h"
#include "ofxXmlSettings.h"


class Model {
  private:
    static map <string, string> xmlSettingsNames;
    static map <string, string> setXMLSettingsNames();

    static map <string, shared_ptr<ofxXmlSettings> > xmlSettings;
    static map <string, shared_ptr<ofxXmlSettings> > setXMLsettings();

  public:
    virtual void setXMLSettingsName() = 0;
    void buildParameters();
    virtual void specificParameters() = 0;
    void setShape();

    shared_ptr<WaveRingVariation> shape;
    shared_ptr<ParticleData> data;

    string xmlSettingsName;

    int shapesNum;
    float radius;
    float width;
    int segments;
    float speedAmp;
    ofVec3f posAmp;
    ofVec3f rotAmp;
    int framesPerCycle;
    float noiseStep;
    float noiseAmount;
    int fadeAmnt;
    bool colMode;
    int saturation;
    int brightness;
    int alpha;

    void draw();
    void update();

    void setPosition(ofPoint _position);

    Model(shared_ptr<ParticleData>& _particleData);

};
#endif
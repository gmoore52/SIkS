#include <vector>
#ifndef SMAWS_DATASET_H
#define SMAWS_DATASET_H

struct SensorData
{
    unsigned SensingRange;
    unsigned CommRange;
    unsigned MoveRange;
};

struct Point{
    unsigned x;
    unsigned y;

    bool operator ==(const Point& other) const
    {
        return (this->x == other.x && this->y == other.y);
    }
};

struct Sensor
{
    Point Position;
    unsigned Power;
};

struct FieldOfInterest
{
    Point TopLeft;
    Point BottomRight;
    unsigned DegreeOfCoverage;
};

struct Dataset
{
    SensorData SenseData;
    Point ScenarioSize;
    std::vector<Sensor> Sensors;
    std::vector<FieldOfInterest> FOI;
};

#endif //SMAWS_DATASET_H

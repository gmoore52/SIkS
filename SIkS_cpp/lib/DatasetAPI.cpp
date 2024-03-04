
#include "DatasetAPI.h"
#include <fstream>
#include <iostream>

namespace SMAWS {

    using json = nlohmann::json;

    Dataset DatasetAPI::LoadDataset(const std::string& datasetPath)
    {
        Dataset returnDataset;
        std::ifstream inFile(datasetPath);
//        json::Reader
        json dataset = json::parse(inFile);


        Point size;
        size.y = dataset["size"][0];
        size.x = dataset["size"][1];

        returnDataset.ScenarioSize = size;

        std::vector<int> sensor_data_vector;
        std::string token;
        std::stringstream  ss(dataset["sensor_data"].get<std::string>());
        while(getline(ss, token, ' '))
        {
            sensor_data_vector.emplace_back(stoi(token));
        }
        SensorData sensorData;
        sensorData.SensingRange = sensor_data_vector[0];
        sensorData.CommRange = sensor_data_vector[1];
        sensorData.MoveRange = sensor_data_vector[2];

        returnDataset.SenseData = sensorData;

//        dataset.get("sensor_data").asString();

        for(auto sensor_string : dataset["sensors"]) {
            Sensor sensor;
            std::vector<int> sensor_vector;
            std::stringstream ss(sensor_string.get<std::string>());
            while(getline(ss, token, ' '))
                sensor_vector.emplace_back(stoi(token));

            sensor.Position.y = sensor_vector[0];
            sensor.Position.x = sensor_vector[1];
            sensor.Power = sensor_vector[2];

            returnDataset.Sensors.emplace_back(sensor);
        }

        for(auto foi_string : dataset["foi"]) {
            FieldOfInterest foi;
            std::vector<int> foi_vector;
            std::stringstream ss(foi_string.get<std::string>());
            while(getline(ss, token, ' '))
                foi_vector.emplace_back(stoi(token));

            foi.TopLeft.x = foi_vector[0];
            foi.TopLeft.y = foi_vector[1];
            foi.BottomRight.x = foi_vector[2];
            foi.BottomRight.y = foi_vector[3];
            foi.DegreeOfCoverage = foi_vector[4];
            returnDataset.FOI.emplace_back(foi);
        }
        return returnDataset;
    }
} // SMAWS
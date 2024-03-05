//#include <glm/matrix.hpp>
#include <Eigen/Core>
#include "DatasetAPI.h"
#ifndef SMAWS_SCENARIOSIMULATOR_H
#define SMAWS_SCENARIOSIMULATOR_H

// Temporary declaration to make sure code works while outlining things

struct State {
    Eigen::MatrixXi CovMat;
    Eigen::MatrixXi DepField;
    Eigen::MatrixXi DesMat;
};

struct ResetVector
{
    std::vector<Eigen::MatrixXi> obs;
    State state;
    std::vector<std::vector<unsigned>> actions;
};

//struct StepVector
//{
//
//    std::vector<std::vector<unsigned>> actions;
//};

namespace SMAWS {

    class ScenarioSimulator {
    public:
        ScenarioSimulator(const std::string&);


        std::vector<Eigen::MatrixXi> GetObs();
        Eigen::MatrixXi GetObsAgent(const unsigned&);
        Eigen::Vector3i GetObsSize();

        State GetState() const;
        Eigen::Vector3i GetStateSize() const;

        std::vector<unsigned> GetAvailableAgentActions(const unsigned&);

        std::vector<std::vector<unsigned>> GetAvailableActions();


        ResetVector Reset();
        ResetVector Step(const std::vector<unsigned>&);

        inline unsigned GetTotalActions() const { return Get_n_Actions()*Get_n_Agents();}
        inline unsigned Get_n_Actions() const {return n_Actions;}
        inline unsigned Get_n_Agents() const {return m_Sensors.size();}

        inline Eigen::MatrixXi GetDeploymentField() const {return m_DeploymentField;}
        inline Eigen::MatrixXi GetCoverageMatrix() const {return m_CoverageMatrix;}
        inline Eigen::MatrixXi GetDesiredMatrix() const {return m_DesiredMatrix;}

    private:
        std::string m_DatasetPath;
        Dataset m_Dataset;
        unsigned n_Actions;
        unsigned m_SizeX;
        unsigned m_SizeY;
        std::vector<Sensor> m_Sensors;
        SensorData m_SenseData;


        Eigen::MatrixXi m_DeploymentField;
        Eigen::MatrixXi m_CoverageMatrix;
        Eigen::MatrixXi m_DesiredMatrix;


        std::vector<Point> ReturnRawActions(const unsigned&);

        void RandomlyDeploySensors();
        void ComputeCoverage();
        void ComputeDeploymentField();

        static void DrawCoverageDisk(Eigen::MatrixXi&, const Point&, const unsigned&);
        static std::vector<Point> FindZeroIndices(const Eigen::MatrixXi&);

    };

} // SMAWS

#endif //SMAWS_SCENARIOSIMULATOR_H

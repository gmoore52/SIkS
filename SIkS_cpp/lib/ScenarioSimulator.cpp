#include <random>
#include <chrono>
#include "ScenarioSimulator.h"

namespace SMAWS {
    void ScenarioSimulator::DrawCoverageDisk(Eigen::MatrixXi& matrix, const Point& point, const unsigned int& radius)
    {
        for(int i = point.x - radius; i<=point.x+radius; ++i)
            for(int j = point.y-radius; j <= point.y + radius; ++j)
                if(i>= 0 && i < matrix.cols() && j >= 0 && j < matrix.rows() &&
                    (i-point.x)*(i-point.x) + (j-point.y)*(j-point.y) <= radius*radius)
                    matrix(j, i) += 1;
    }

    std::vector<Point> ScenarioSimulator::FindZeroIndices(const Eigen::MatrixXi& matrix)
    {
        std::vector<Point> indices;
        for(int x = 0; x < matrix.cols(); x++)
            for(int y = 0; y < matrix.rows(); y++)
                if(matrix(y, x) == 0)
                    indices.emplace_back(x, y);

        return indices;
    }

    ScenarioSimulator::ScenarioSimulator(const std::string& dataset_path) :
    m_DatasetPath(dataset_path)
//        m_SizeX(x_size), m_SizeY(y_size), m_SenseData(sense_data)
    {

        m_Dataset = DatasetAPI::LoadDataset(m_DatasetPath);

        m_SizeX = m_Dataset.ScenarioSize.x;
        m_SizeY = m_Dataset.ScenarioSize.y;

        m_Sensors = m_Dataset.Sensors;
        m_SenseData = m_Dataset.SenseData;


        m_DeploymentField = Eigen::MatrixXi::Zero(m_SizeY, m_SizeX);

        m_CoverageMatrix = Eigen::MatrixXi::Zero(m_SizeY, m_SizeX);

        m_DesiredMatrix = Eigen::MatrixXi::Zero(m_SizeY, m_SizeX);

        n_Actions = 0;

        // First run midpoint circle once to define the number of actions
        unsigned radius = m_SenseData.MoveRange;
        int f = 1-radius;
        int ddf_x = 1;
        int ddf_y = -2*radius;
        int x = 0;
        int y = radius;
        // Add 4 actions for each point on the x/y axes around each sensor and 1 action for the zero cost action
        n_Actions += 5;


        while(x < y)
        {
            if(f>=0)
            {
                y--;
                ddf_y += 2;
                f += ddf_y;
            }
            x++;
            ddf_x += 2;
            f+= ddf_x;
            n_Actions += 8;
        }

//        ComputeCoverage();
        Reset();
    }

    ResetVector ScenarioSimulator::Reset()
    {
        m_Dataset = DatasetAPI::LoadDataset(m_DatasetPath);
//        auto Dataset = API::LoadDataset(m_DatasetName);
        m_Sensors.clear();
        m_SenseData = m_Dataset.SenseData;

        m_Sensors = m_Dataset.Sensors;

        ComputeDeploymentField();
        ComputeCoverage();

        m_DesiredMatrix = Eigen::MatrixXi::Zero(m_SizeY, m_SizeX);
        for(auto foi : m_Dataset.FOI)
            for (int x = foi.TopLeft.x; x < foi.BottomRight.x; x++)
                for (int y = foi.TopLeft.y; y < foi.BottomRight.y; y++)
                    m_DesiredMatrix(y, x) = foi.DegreeOfCoverage;

        return {GetObs(), GetState(), GetAvailableActions()};
//        for(auto sensor : )
    }

    ResetVector ScenarioSimulator::Step(const std::vector<unsigned>& actions)
    {

        int totalEnergyReward = 0;
        int totalCoverageReward = 0;


        for(int i = 0; i < actions.size(); i++)
        {
            auto action = ReturnRawActions(i)[actions[i]];

            Point zeroCostAction = m_Sensors[i].Position;

            // TODO: Add codition for if the sensor is out of power to not move
            if(m_DeploymentField(action.y, action.x) != 0)
                action = zeroCostAction;


            m_DeploymentField(zeroCostAction.y, zeroCostAction.x) = 0;
            m_DeploymentField(action.y, action.x) = 1;
            m_Sensors[i].Position = action;
        }

        ComputeDeploymentField();
        ComputeCoverage();

        Eigen::MatrixXi RewardMatrix = m_CoverageMatrix - m_DesiredMatrix;

        for(auto foi : m_Dataset.FOI)
            for(int x = foi.TopLeft.x; x < foi.BottomRight.x; x++)
                for(int y = foi.TopLeft.y; y < foi.BottomRight.y; y++)
                    totalCoverageReward += (RewardMatrix(y, x) >= 0) ? RewardMatrix(y, x) : 0;


        int finalReward = totalCoverageReward + totalEnergyReward;

        return {GetObs(), GetState(), GetAvailableActions()};

    }

    Eigen::MatrixXi ScenarioSimulator::GetObsAgent(const unsigned int& agent_id)
    {
        Sensor& sensor = m_Sensors[agent_id];

        unsigned ObsSizeX = 1+(m_SenseData.SensingRange+m_SenseData.MoveRange)*2;
        unsigned ObsSizeY = 1+(m_SenseData.SensingRange+m_SenseData.MoveRange)*2;
        unsigned ObsPosX = sensor.Position.x - (ObsSizeX/2);
        unsigned ObsPosY = sensor.Position.y - (ObsSizeY/2);

        Eigen::MatrixXi covMatrix = Eigen::MatrixXi::Zero(ObsSizeY, ObsSizeX);
        Eigen::MatrixXi posMatrix = Eigen::MatrixXi::Zero(ObsSizeY, ObsSizeX);

        unsigned borderSizeX = (ObsSizeX*2)+m_SizeX;
        unsigned borderSizeY = (ObsSizeY*2)+m_SizeY;

        Eigen::MatrixXi BorderCoverageMatrix = Eigen::MatrixXi::Constant(borderSizeY,
                                                                         borderSizeX, -1);
        Eigen::MatrixXi BorderDeploymentMatrix = Eigen::MatrixXi::Constant(borderSizeY,
                                                                           borderSizeX, 2);

        std::vector<int> index_list_x, index_list_y;
        for(int x = borderSizeX, y = borderSizeY; x < borderSizeX && y < borderSizeY; x++, y++)
            index_list_x.emplace_back(x), index_list_y.emplace_back(y);


        BorderCoverageMatrix(index_list_y, index_list_x) =
                m_CoverageMatrix(index_list_y, index_list_x)
                - m_DesiredMatrix(index_list_y, index_list_x);

        BorderDeploymentMatrix(index_list_y, index_list_x) =
                    m_DeploymentField(index_list_y, index_list_x);


        unsigned borderPosX = ObsPosX + ObsSizeX;
        unsigned borderPosY = ObsPosY + ObsSizeY;
        index_list_x.clear();
        index_list_y.clear();
        for(int x = borderPosX-1, y = borderPosY-1; x < borderPosX + ObsSizeX
                                && y < borderSizeY + ObsSizeY; x++, y++)
            index_list_x.emplace_back(x), index_list_y.emplace_back(y);


        covMatrix = BorderCoverageMatrix(index_list_y, index_list_x);
        posMatrix = BorderDeploymentMatrix(index_list_y, index_list_x);

        return covMatrix;
    }

    std::vector<Eigen::MatrixXi> ScenarioSimulator::GetObs()
    {
        std::vector<Eigen::MatrixXi> returnVector;
        for(unsigned i = 0; i < m_Sensors.size(); i++)
            returnVector.emplace_back(GetObsAgent(i));

        return returnVector;
    }

    Eigen::Vector3i ScenarioSimulator::GetObsSize()
    {
//        std::vector<Eigen::Vector3i> obs_size;

        Eigen::MatrixXi first = GetObs().front();
        unsigned&& n_obs = GetObs().size();

        return {n_obs, first.rows(), first.cols()};
    }

    State ScenarioSimulator::GetState() const
    {
        return {GetCoverageMatrix(), GetDeploymentField(), GetDesiredMatrix()};
    }

    Eigen::Vector3i ScenarioSimulator::GetStateSize() const
    {
        return {3, GetCoverageMatrix().rows(), GetCoverageMatrix().cols()};
    }

    std::vector<std::vector<unsigned int>> ScenarioSimulator::GetAvailableActions()
    {
        std::vector<std::vector<unsigned>> TotalAvailableActions;

        for(int i = 0; i < m_Sensors.size(); i++)
            TotalAvailableActions.emplace_back(GetAvailableAgentActions(i));

        return TotalAvailableActions;
    }

    std::vector<unsigned int> ScenarioSimulator::GetAvailableAgentActions(const unsigned int& agent_id)
    {

        std::vector<Point> actionList;
        std::vector<unsigned> FinalActionsInt;

        Sensor& sensor = m_Sensors[agent_id];
        unsigned xPos = sensor.Position.x;
        unsigned yPos = sensor.Position.y;

        actionList = ReturnRawActions(agent_id);

        Point zero_cost(xPos, yPos);

        // Encode the actions by assigning each action its own unique index
        for(int i = 0; i < actionList.size(); i++)
        {
            if(actionList[i] == zero_cost)
            FinalActionsInt.emplace_back(0);
            else
            FinalActionsInt.emplace_back(i);
        }

        return FinalActionsInt;
    }

    std::vector<Point> ScenarioSimulator::ReturnRawActions(const unsigned int& agent_id)
    {
        std::vector<Point> actionList;

        Sensor& sensor = m_Sensors[agent_id];

        unsigned xPos, yPos;
        xPos = sensor.Position.x;
        yPos = sensor.Position.y;

        // Add the zero cost action to the action list
        actionList.emplace_back(xPos, yPos);

        // TODO: Add a option here for lists of negative actions

        unsigned radius = m_SenseData.MoveRange;
        int f = 1-radius;
        int ddf_x = 1;
        int ddf_y = -2*radius;
        int x = 0;
        int y = radius;
        actionList.emplace_back(xPos, yPos+radius);
        actionList.emplace_back(xPos, yPos-radius);
        actionList.emplace_back(xPos+radius, yPos);
        actionList.emplace_back(xPos-radius, yPos);


        while(x < y)
        {
            if(f>=0)
            {
                y--;
                ddf_y += 2;
                f += ddf_y;
            }
            x++;
            ddf_x += 2;
            f+= ddf_x;
            actionList.emplace_back(xPos + x, yPos + y);
            actionList.emplace_back(xPos - x, yPos + y);
            actionList.emplace_back(xPos + x, yPos - y);
            actionList.emplace_back(xPos - x, yPos - y);
            actionList.emplace_back(xPos + y, yPos + x);
            actionList.emplace_back(xPos - y, yPos + x);
            actionList.emplace_back(xPos + y, yPos - x);
            actionList.emplace_back(xPos - y, yPos - x);

        }


        for(auto action = actionList.begin(); action != actionList.end();)
        {
            if(action->x < 0 || action->x >= m_SizeX || action->y < 0 || action->y >= m_SizeY)
                action = actionList.erase(action);
            else
                action++;
        }

        // Add zero action until the vector is the proper size
        while(actionList.size() < n_Actions)
        {
            actionList.emplace_back(xPos, yPos);
        }

        return actionList;
    }

    void ScenarioSimulator::RandomlyDeploySensors()
    {
        auto valid_indices = ScenarioSimulator::FindZeroIndices(m_DeploymentField);
        std::uniform_int_distribution<std::mt19937::result_type> udist(0, valid_indices.size()-1);
        std::mt19937 rng;

        for(auto &sensor : m_Sensors)
        {
            auto seed_val = std::chrono::system_clock::now().time_since_epoch().count();
            rng.seed(seed_val);

            unsigned random_index = udist(rng);
            auto point = valid_indices.at(random_index);

            sensor.Position = point;
            valid_indices.erase(valid_indices.begin() + random_index);
        }

        ComputeDeploymentField();
        ComputeCoverage();
    }

    void ScenarioSimulator::ComputeCoverage()
    {
        m_CoverageMatrix = Eigen::MatrixXi::Zero(m_SizeY, m_SizeX);
        // Use static method to draw the disk
        for(auto sensor : m_Sensors)
            ScenarioSimulator::DrawCoverageDisk(m_CoverageMatrix,
                                                sensor.Position, m_SenseData.SensingRange);

    }

    void ScenarioSimulator::ComputeDeploymentField()
    {
        m_DeploymentField = Eigen::MatrixXi::Zero(m_SizeY, m_SizeX);
        for(auto sensor : m_Sensors)
        {
            m_DeploymentField(sensor.Position.y, sensor.Position.x) = 1;
        }
    }

} // SMAWS
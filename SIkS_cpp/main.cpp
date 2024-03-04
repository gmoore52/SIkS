#include "lib/ScenarioSimulator.h"
#include <iostream>
#include <chrono>
#include <random>


int main()
{
    const int STEPS = 10;



//    SMAWS::ScenarioSimulator simulator(100, 100, {20, 20});
    std::vector<double> times;

    for(int x = 1; x <= 10; x++) {
        auto begin = std::chrono::high_resolution_clock::now();
        SMAWS::ScenarioSimulator simulator("newTest12.json");

        std::uniform_int_distribution<std::mt19937::result_type> udist(0, simulator.Get_n_Actions()-1);
        std::mt19937 rng;
        for (int _ = 0; _ < STEPS*x; _++) {
            std::vector<unsigned> actions;

            for (int a_id = 0; a_id < simulator.Get_n_Actions(); a_id++) {
                auto avail_actions = simulator.GetAvailableAgentActions(a_id);

                auto seed_val = std::chrono::system_clock::now().time_since_epoch().count();
                rng.seed(seed_val);

                int random_index = udist(rng);
                auto action = avail_actions[random_index];

                actions.emplace_back(action);
                auto obs = simulator.GetObsAgent(a_id);
            }

            auto data = simulator.Step(actions);
            auto state = simulator.GetState();
            simulator.GetObs();
//            std::cout << "Step " << std::to_string(_) << " complete" << std::endl;

        }

        auto time_since = duration_cast<std::chrono::microseconds>(std::chrono::high_resolution_clock::now() - begin);
        std::cout << "Program takes approximately " << time_since.count() <<
        " seconds to complete for " << std::to_string(STEPS*x) << " steps" << std::endl;




    }


//    std::cout << simulator.GetCoverageMatrix() << std::endl;
//    glm::mat<3,3,int,glm::defaultp> matrix;
}
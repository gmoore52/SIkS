#include <glm/matrix.hpp>
#ifndef SMAWS_SCENARIOSIMULATOR_H
#define SMAWS_SCENARIOSIMULATOR_H

namespace SMAWS {

    template <unsigned SIZE_X, unsigned SIZE_Y> class ScenarioSimulator {
    public:

        inline glm::mat<SIZE_X, SIZE_Y, int, glm::defaultp> GetDeploymentField() const {return m_DeploymentField;}
        inline glm::mat<SIZE_X, SIZE_Y, int, glm::defaultp> GetCoverageMatrix() const {return m_CoverageMatrix;}
        inline glm::mat<SIZE_X, SIZE_Y, int, glm::defaultp> GetDesiredMatrix() const {return m_DesiredMatrix;}

    private:

        glm::mat<SIZE_X, SIZE_Y, int, glm::defaultp> m_DeploymentField;
        glm::mat<SIZE_X, SIZE_Y, int, glm::defaultp> m_CoverageMatrix;
        glm::mat<SIZE_X, SIZE_Y, int, glm::defaultp> m_DesiredMatrix;
    };

} // SMAWS

#endif //SMAWS_SCENARIOSIMULATOR_H

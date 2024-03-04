#include <nlohmann/json.hpp>
#include "Dataset.h"
#ifndef SMAWS_DATASETAPI_H
#define SMAWS_DATASETAPI_H


namespace SMAWS {

    class DatasetAPI {
    public:
        static Dataset LoadDataset(const std::string&);
    };

} // SMAWS

#endif //SMAWS_DATASETAPI_H

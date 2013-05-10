import pybindgen as pg
import sys

# model parameter config

mod = pg.Module('sofia')
ns = mod.add_cpp_namespace('sofia_ml')

mod.add_include('"sf-weight-vector.h"')
mod.add_include('"sofia-ml-methods.h"')
mod.add_include('"sofia.h"')
mod.add_include('<string>')
mod.add_include('<vector>')
mod.add_include('<cstdlib>')

sf_weight_vector = mod.add_class('SfWeightVector')
sf_weight_vector.add_constructor([pg.param('int', 'dimensionality')])

sf_data_set = mod.add_class('SfDataSet')
sf_data_set.add_constructor([pg.param('const std::string &', 'file_name'),
                             pg.param('bool', 'use_bias_term')])

vecf = mod.add_container('std::vector<float>', 'float', 'vector', custom_name="vecf")

mod.add_function('srand', None, [pg.param('unsigned int', 'seed')])

mod.add_function('TrainModel',
                 pg.retval('SfWeightVector *', caller_owns_return=True),
                 [pg.param('const SfDataSet&', 'training_data'),
                  pg.param('float', 'lambda')])

ns.add_function('SvmPredictionsOnTestSet', pg.retval('std::vector<float>'),
                [pg.param('const SfDataSet&', 'test_data'),
                 pg.param('const SfWeightVector&', 'w')])

ns.add_function('LogisticPredictionsOnTestSet', pg.retval('std::vector<float>'),
                [pg.param('const SfDataSet&', 'test_data'),
                 pg.param('const SfWeightVector&', 'w')])

ns.add_function('SvmObjective', pg.retval('float'),
                [pg.param('const SfDataSet&', 'test_data'),
                 pg.param('const SfWeightVector&', 'w'),
                 pg.param('float', 'lambda')])

mod.add_function('SaveModelToFile', None, [pg.param('std::string', 'file_name'),
                                           pg.param('SfWeightVector*', 'w', transfer_ownership=False)])

mod.add_function("LoadModelFromFile", pg.retval("SfWeightVector *", caller_owns_return=True),
                 [pg.param('const std::string &', 'file_name')]);

mod.generate(sys.stdout)

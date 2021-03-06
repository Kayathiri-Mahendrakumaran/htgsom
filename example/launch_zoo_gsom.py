import time
import sys
from os import makedirs
from os.path import exists
sys.path.append('../../')

from util import input_parser as Parser
from util import utilities as Utils
from util import display as Display_Utils

from params import params as Params
from core import core_controller as Core

# Config
input_filename = "data/zoo.txt"
output_save_filename = 'zoo_data'
output_save_location = 'output/'
if not exists(output_save_location):
    makedirs(output_save_location)

SF = 0.7
forget_threshold = 1000
plot_output_name = output_save_location + output_save_filename + str(SF) + '_mage_' + str(forget_threshold) + 'itr'


if __name__ == '__main__':

    print('Start GSOM algorithm.')

    gsom_params = Params.GSOMParameters(SF, 50, 10, distance=Params.DistanceFunction.EUCLIDEAN,
                                        forget_itr_count=forget_threshold)
    generalise_params = Params.GeneraliseParameters(gsom_params)

    # Process the input files
    input_vector_database, labels, classes = Parser.InputParser.parse_input_zoo_data(input_filename, None)

    # Process the clustering algorithm algorithm
    controller = Core.Controller(generalise_params)
    controller_start = time.time()
    result_dict = controller.run(input_vector_database)
    print('Algorithms completed in', round(time.time() - controller_start, 2), '(s)')
    Utils.Utilities.save_object(result_dict, output_save_location + output_save_filename)

    # Display
    display = Display_Utils.Display(result_dict[0]['gsom'])
    display.setup_labels_for_gsom_nodemap(labels, 1, 'Names of animals', output_save_location + 'gsom_names_' + str(SF))
    display.setup_labels_for_gsom_nodemap(classes, 2, 'Categories of animals', output_save_location + 'gsom_categories_' + str(SF))

    print('Visualisation saved in output folder.')

# import json
import container_scrape
import container_utils
import container_search
# from fractions import Fraction
# import unicodedata


class ContainerScrapeCleanAggOrg:

    def __init__(self, scrape_bool = [False, False]):

        """
        This class runs the scraping, cleaning, aggregation, and organization all in one place.

        scrape_bool is set to false and only runs if given a True agrument, because it takes a long time and deletes a file, so I don't want to run it by accident.

        """
        if scrape_bool[0]:
            container_scrape.ContainerScrape_ikea()
        if scrape_bool[1]:
            container_scrape.ContainerScrape_conStore()

        my_c_conStore = container_utils.ContainerClean_conStore()
        my_c_ikea=container_utils.ContainerClean_ikea()
        
        my_c_conStore.create_new_dimensions()
        my_c_ikea.create_new_dimensions()

        my_c_conStore.write_file()
        my_c_ikea.write_file()

        my_agg = container_utils.Container_Aggregate()
        my_org= container_utils.Container_Organize()
        my_org.organize_new_dimensions()
        my_org.write_file()

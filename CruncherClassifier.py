import zlib
from bs4 import BeautifulSoup, NavigableString, Comment
import json
import re
import sys 

def to_lower_case(string):
    return string.lower()

def remove_extra_whitespace(string):
    return re.sub("\t+", " ", re.sub("\n+", " ", re.sub(" +", " ", string)))
    #return re.sub("\s+", " ", string)

class CruncherClassifier():
    def __init__(self, source_file_dir, selector_mapping, result_dir):
        self.source_file_dir = source_file_dir
        
        with open(selector_mapping, encoding="utf-8") as f:
            selector_dict = json.loads(f.read())
            self.selectors = selector_dict["mapping"].items()

            self.selector_to_content = { key[0]: [] for key in self.selectors }
            self.selector_entropies = { key[0]: 0 for key in self.selectors }

            self.sources = selector_dict["members"]
            self.num_of_non_selectors = len(next(iter(self.sources.values()))) - len(self.selectors)

        self.result_filepath = f"{ result_dir }/"

    def _dom_query_to_content(self, query_arr):
        if not len(query_arr):
            return ""

        result = ""

        for tag in query_arr:
            result += tag.getText() + " " 

        return result

    def _clean_content(self):
        for key in self.selector_to_content:
            self.selector_to_content[key] = to_lower_case(remove_extra_whitespace(self.selector_to_content[key]))

    def _sort_content(self):
        for key in self.selector_to_content:
            self.selector_to_content[key] = sorted(self.selector_to_content[key])

    def _save_content(self):
        for key in self.selector_to_content:
            with open(f"{ self.result_filepath }{ key }", "w") as f:
                self.selector_to_content[key] = "\n".join(self.selector_to_content[key])
                f.write(self.selector_to_content[key])
                f.close()

    def extract_content(self):
        max_ = len(self.sources.keys())
        counter = 0

        test_sources = ['uutiset-3-10629758.html', 'uutiset-3-11382627.html',
        'uutiset-3-10580429.html', 'uutiset-3-11831776.html',
        'uutiset-3-8742701.html', 'uutiset-3-11889938.html',
        'uutiset-3-11974434.html', 'uutiset-3-8994581.html',
        'uutiset-3-10292280.html', 'uutiset-3-11007968.html',
        'uutiset-3-8961570.html', 'uutiset-3-11537184.html',
        'uutiset-3-10787554.html', 'uutiset-3-10882907.html',
        'uutiset-3-11435960.html', 'uutiset-3-9491795.html',
        'uutiset-3-11617083.html', 'uutiset-3-11875657.html',
        'uutiset-3-10385179.html', 'uutiset-3-10490500.html',
        'uutiset-3-5964016.html', 'uutiset-3-11761266.html',
        'uutiset-3-11586547.html', 'uutiset-3-11695608.html',
        'uutiset-3-9057304.html', 'uutiset-3-8665212.html',
        'uutiset-3-10939320.html', 'uutiset-3-5398830.html',
        'uutiset-3-9966336.html', 'uutiset-3-11602436.html',
        'uutiset-3-11075067.html', 'uutiset-3-7553271.html',
        'uutiset-3-11745389.html', 'uutiset-3-11284697.html',
        'uutiset-3-9560440.html', 'uutiset-3-11283609.html',
        'uutiset-3-11288047.html', 'uutiset-3-11133793.html',
        'uutiset-3-9356106.html', 'uutiset-3-11392462.html',
        'uutiset-3-11809887.html', 'uutiset-3-8885532.html',
        'uutiset-3-11056365.html', 'uutiset-3-11232858.html',
        'uutiset-3-9681516.html', 'uutiset-3-11554860.html',
        'uutiset-3-11839067.html', 'uutiset-3-10920035.html',
        'uutiset-3-11741048.html', 'uutiset-3-5218114.html',
        'uutiset-3-8701491.html', 'uutiset-3-9907477.html',
        'uutiset-3-5969530.html', 'uutiset-3-11683315.html',
        'uutiset-3-9980408.html', 'uutiset-3-11861706.html',
        'uutiset-3-7240426.html', 'uutiset-3-8602912.html',
        'uutiset-3-11808684.html', 'uutiset-3-8492665.html',
        'uutiset-3-7296276.html', 'uutiset-3-11534087.html',
        'uutiset-3-10050630.html', 'uutiset-3-9357000.html',
        'uutiset-3-11922534.html', 'uutiset-3-11717843.html',
        'uutiset-3-11965600.html', 'uutiset-3-10908767.html',
        'uutiset-3-11921907.html', 'uutiset-3-11527309.html',
        'uutiset-3-11842871.html', 'uutiset-3-6236515.html',
        'uutiset-3-11224377.html', 'uutiset-3-11216177.html',
        'uutiset-3-5595368.html', 'uutiset-3-9727811.html',
        'uutiset-3-11817387.html', 'uutiset-3-10634838.html',
        'uutiset-3-8103426.html', 'uutiset-3-11988931.html',
        'uutiset-3-11802732.html', 'uutiset-3-10560111.html',
        'uutiset-3-11441205.html', 'uutiset-3-5902665.html',
        'uutiset-3-8765763.html', 'uutiset-3-7435007.html',
        'uutiset-3-11732746.html', 'uutiset-3-11854566.html',
        'uutiset-3-8679882.html', 'uutiset-3-10823682.html',
        'uutiset-3-10118841.html', 'uutiset-3-8668085.html',
        'uutiset-3-11263453.html', 'uutiset-3-11957320.html',
        'uutiset-3-6455123.html', 'uutiset-3-11017548.html',
        'uutiset-3-11137540.html', 'uutiset-3-11968819.html',
        'uutiset-3-11701266.html', 'uutiset-3-11143243.html',
        'uutiset-3-11642712.html', 'uutiset-3-11818123.html',
        'uutiset-3-11068135.html', 'uutiset-3-11282240.html',
        'uutiset-3-10419914.html', 'uutiset-3-8665821.html',
        'uutiset-3-8695572.html', 'uutiset-3-10802553.html',
        'uutiset-3-11881198.html', 'uutiset-3-11331718.html',
        'uutiset-3-7037145.html', 'uutiset-3-11724491.html',
        'uutiset-3-11298056.html', 'uutiset-3-11841494.html',
        'uutiset-3-11635267.html', 'uutiset-3-11554445.html',
        'uutiset-3-11965193.html', 'uutiset-3-10408647.html',
        'uutiset-3-9694437.html', 'uutiset-3-10924732.html',
        'uutiset-3-11969107.html', 'uutiset-3-11288937.html',
        'uutiset-3-11731074.html', 'uutiset-3-11913337.html',
        'uutiset-3-11405718.html', 'uutiset-3-11848911.html',
        'uutiset-3-11380352.html', 'uutiset-3-11133360.html',
        'uutiset-3-11919984.html', 'uutiset-3-11200292.html',
        'uutiset-3-9191420.html', 'uutiset-3-11358614.html',
        'uutiset-3-7695469.html', 'uutiset-3-10195372.html',
        'uutiset-3-11534374.html', 'uutiset-3-8106383.html',
        'uutiset-3-11188999.html', 'uutiset-3-11772699.html',
        'uutiset-3-10693107.html', 'uutiset-3-11925412.html',
        'uutiset-3-11633565.html', 'uutiset-3-11337652.html',
        'uutiset-3-11236847.html', 'uutiset-3-11441224.html',
        'uutiset-3-11728907.html', 'uutiset-3-11947144.html',
        'uutiset-3-9774003.html', 'uutiset-3-11642525.html',
        'uutiset-3-5462903.html', 'uutiset-3-10607982.html',
        'uutiset-3-11781827.html', 'uutiset-3-10551566.html',
        'uutiset-3-11261427.html', 'uutiset-3-11220567.html',
        'uutiset-3-10613151.html', 'uutiset-3-6697558.html',
        'uutiset-3-11265130.html', 'uutiset-3-11037469.html',
        'uutiset-3-11851042.html', 'uutiset-3-10687526.html',
        'uutiset-3-11901696.html', 'uutiset-3-11679091.html',
        'uutiset-3-5746774.html', 'uutiset-3-11713346.html',
        'uutiset-3-11913658.html', 'uutiset-3-10199545.html',
        'uutiset-3-11578884.html', 'uutiset-3-6694082.html',
        'uutiset-3-11891249.html', 'uutiset-3-5135299.html',
        'uutiset-3-11421883.html', 'uutiset-3-11817162.html',
        'uutiset-3-5128906.html', 'uutiset-3-11298272.html',
        'uutiset-3-5121602.html', 'uutiset-3-9410364.html',
        'uutiset-3-11732121.html', 'uutiset-3-9749602.html',
        'uutiset-3-10719169.html', 'uutiset-3-9526435.html',
        'uutiset-3-11810851.html', 'uutiset-3-11862591.html',
        'uutiset-3-11701262.html', 'uutiset-3-7720481.html',
        'uutiset-3-8699313.html', 'uutiset-3-11505539.html',
        'uutiset-3-10908617.html', 'uutiset-3-10848295.html',
        'uutiset-3-11839260.html', 'uutiset-3-6693618.html',
        'uutiset-3-9699713.html', 'uutiset-3-11734701.html',
        'uutiset-3-11937769.html', 'uutiset-3-7359536.html',
        'uutiset-3-5611054.html', 'uutiset-3-11785851.html',
        'uutiset-3-8719782.html', 'uutiset-3-11935726.html',
        'uutiset-3-5176435.html', 'uutiset-3-11860484.html',
        'uutiset-3-11723790.html', 'uutiset-3-8035070.html',
        'uutiset-3-11653617.html', 'uutiset-3-7721278.html',
        'uutiset-3-11570527.html', 'uutiset-3-7521873.html',
        'uutiset-3-11291697.html', 'uutiset-3-11958567.html',
        'uutiset-3-11363848.html', 'uutiset-3-11905062.html',
        'uutiset-3-7394913.html', 'uutiset-3-10603657.html',
        'uutiset-3-9484212.html', 'uutiset-3-11731128.html',
        'uutiset-3-11445297.html', 'uutiset-3-5749172.html',
        'uutiset-3-11837950.html', 'uutiset-3-11981187.html',
        'uutiset-3-11746660.html', 'uutiset-3-5327193.html',
        'uutiset-3-11990835.html', 'uutiset-3-11178788.html',
        'uutiset-3-11821976.html', 'uutiset-3-8870099.html',
        'uutiset-3-11780531.html', 'uutiset-3-10916997.html',
        'uutiset-3-8840008.html', 'uutiset-3-8526878.html',
        'uutiset-3-11620669.html', 'uutiset-3-5856095.html',
        'uutiset-3-5084000.html', 'uutiset-3-11988727.html',
        'uutiset-3-6048049.html', 'uutiset-3-10159317.html',
        'uutiset-3-11968945.html', 'uutiset-3-11811144.html',
        'uutiset-3-11895823.html', 'uutiset-3-11960223.html',
        'uutiset-3-11345129.html', 'uutiset-3-10836458.html',
        'uutiset-3-10911419.html', 'uutiset-3-7851114.html',
        'uutiset-3-10318116.html', 'uutiset-3-11154674.html',
        'uutiset-3-11721177.html', 'uutiset-3-11797556.html',
        'uutiset-3-5136576.html', 'uutiset-3-8518342.html',
        'uutiset-3-7866831.html', 'uutiset-3-10682220.html',
        'uutiset-3-11643743.html', 'uutiset-3-11619992.html',
        'uutiset-3-9856934.html', 'uutiset-3-9940159.html',
        'uutiset-3-11876604.html', 'uutiset-3-10932684.html',
        'uutiset-3-11697168.html', 'uutiset-3-11715775.html',
        'uutiset-3-11974920.html', 'uutiset-3-10023992.html',
        'uutiset-3-11657380.html', 'uutiset-3-11715031.html',
        'uutiset-3-10612678.html', 'uutiset-3-9325361.html',
        'uutiset-3-9367326.html', 'uutiset-3-10395654.html',
        'uutiset-3-11840267.html', 'uutiset-3-11968811.html',
        'uutiset-3-11251575.html', 'uutiset-3-11899276.html',
        'uutiset-3-7720564.html', 'uutiset-3-11386858.html',
        'uutiset-3-11840004.html', 'uutiset-3-11160559.html',
        'uutiset-3-5984685.html', 'uutiset-3-9525186.html',
        'uutiset-3-11720360.html', 'uutiset-3-10190377.html',
        'uutiset-3-8358260.html', 'uutiset-3-11110545.html',
        'uutiset-3-11824082.html', 'uutiset-3-11636963.html',
        'uutiset-3-11702003.html', 'uutiset-3-11817013.html',
        'uutiset-3-11912168.html', 'uutiset-3-11358902.html',
        'uutiset-3-11700593.html', 'uutiset-3-11435729.html',
        'uutiset-3-11717990.html', 'uutiset-3-11901036.html',
        'uutiset-3-10972010.html', 'uutiset-3-9055683.html',
        'uutiset-3-11761642.html', 'uutiset-3-11910986.html',
        'uutiset-3-5684209.html', 'uutiset-3-10830581.html',
        'uutiset-3-6833892.html', 'uutiset-3-11988861.html',
        'uutiset-3-10568958.html', 'uutiset-3-9613719.html',
        'uutiset-3-11146680.html', 'uutiset-3-11874917.html',
        'uutiset-3-11148465.html', 'uutiset-3-9543832.html',
        'uutiset-3-9537409.html', 'uutiset-3-11666689.html',
        'uutiset-3-11563790.html', 'uutiset-3-11374586.html',
        'uutiset-3-7739442.html', 'uutiset-3-11650136.html',
        'uutiset-3-11732488.html', 'uutiset-3-7291763.html',
        'uutiset-3-10380288.html', 'uutiset-3-11014008.html',
        'uutiset-3-5220326.html', 'uutiset-3-11838933.html',
        'uutiset-3-7312619.html', 'uutiset-3-10400124.html',
        'uutiset-3-11739621.html', 'uutiset-3-11991687.html',
        'uutiset-3-6811986.html', 'uutiset-3-9683256.html',
        'uutiset-3-11845323.html', 'uutiset-3-11961682.html',
        'uutiset-3-11731924.html', 'uutiset-3-7315979.html',
        'uutiset-3-5053555.html', 'uutiset-3-8558608.html',
        'uutiset-3-11115306.html', 'uutiset-3-9475300.html',
        'uutiset-3-11300232.html', 'uutiset-3-11086134.html',
        'uutiset-3-11750960.html', 'uutiset-3-11991493.html',
        'uutiset-3-11185118.html', 'uutiset-3-5057347.html',
        'uutiset-3-9320445.html', 'uutiset-3-11428310.html',
        'uutiset-3-11628668.html', 'uutiset-3-11255990.html',
        'uutiset-3-11792885.html', 'uutiset-3-11934239.html',
        'uutiset-3-11854660.html', 'uutiset-3-11306302.html',
        'uutiset-3-11263307.html', 'uutiset-3-9284326.html',
        'uutiset-3-11208211.html', 'uutiset-3-10053715.html',
        'uutiset-3-10913593.html', 'uutiset-3-7544167.html',
        'uutiset-3-11584845.html', 'uutiset-3-11573775.html',
        'uutiset-3-10920916.html', 'uutiset-3-11779626.html',
        'uutiset-3-5811950.html', 'uutiset-3-9990377.html',
        'uutiset-3-11293650.html', 'uutiset-3-11423457.html',
        'uutiset-3-11259208.html', 'uutiset-3-11877319.html',
        'uutiset-3-11740930.html', 'uutiset-3-10574927.html',
        'uutiset-3-9545402.html', 'uutiset-3-11814529.html',
        'uutiset-3-11680202.html', 'uutiset-3-11857138.html',
        'uutiset-3-10922513.html', 'uutiset-3-11721238.html',
        'uutiset-3-11988972.html', 'uutiset-3-5405822.html',
        'uutiset-3-11701690.html', 'uutiset-3-11698143.html',
        'uutiset-3-11942036.html', 'uutiset-3-5595668.html',
        'uutiset-3-11837241.html', 'uutiset-3-10629956.html',
        'uutiset-3-11728265.html', 'uutiset-3-11988806.html',
        'uutiset-3-10600309.html', 'uutiset-3-11908212.html',
        'uutiset-3-10928067.html', 'uutiset-3-10197084.html',
        'uutiset-3-11442936.html', 'uutiset-3-10633008.html',
        'uutiset-3-5380048.html', 'uutiset-3-9343590.html',
        'uutiset-3-10787841.html', 'uutiset-3-11744091.html',
        'uutiset-3-5107758.html', 'uutiset-3-11876899.html',
        'uutiset-3-11574083.html', 'uutiset-3-11818154.html',
        'uutiset-3-11877370.html', 'uutiset-3-11986561.html',
        'uutiset-3-11242831.html', 'uutiset-3-9226290.html',
        'uutiset-3-6115298.html', 'uutiset-3-10670308.html',
        'uutiset-3-7790855.html', 'uutiset-3-10729107.html',
        'uutiset-3-11893988.html', 'uutiset-3-6908677.html',
        'uutiset-3-10694539.html', 'uutiset-3-11880391.html',
        'uutiset-3-11104327.html', 'uutiset-3-8668557.html',
        'uutiset-3-8377882.html', 'uutiset-3-9732110.html',
        'uutiset-3-11863839.html', 'uutiset-3-11075616.html',
        'uutiset-3-10961171.html', 'uutiset-3-11476119.html',
        'uutiset-3-10813624.html', 'uutiset-3-11777033.html',
        'uutiset-3-11896237.html', 'uutiset-3-6663597.html',
        'uutiset-3-9184080.html', 'uutiset-3-10570754.html',
        'uutiset-3-10919901.html', 'uutiset-3-8319572.html',
        'uutiset-3-11325508.html', 'uutiset-3-11477592.html',
        'uutiset-3-11922938.html', 'uutiset-3-5971040.html',
        'uutiset-3-11360823.html', 'uutiset-3-11685076.html',
        'uutiset-3-11904865.html', 'uutiset-3-11535242.html',
        'uutiset-3-11913486.html', 'uutiset-3-8383653.html',
        'uutiset-3-10500636.html', 'uutiset-3-11979295.html',
        'uutiset-3-9535312.html', 'uutiset-3-11590302.html',
        'uutiset-3-5935477.html', 'uutiset-3-10381137.html',
        'uutiset-3-11441870.html', 'uutiset-3-11757391.html',
        'uutiset-3-11606242.html', 'uutiset-3-11991593.html',
        'uutiset-3-7839754.html', 'uutiset-3-11896412.html',
        'uutiset-3-11094792.html', 'uutiset-3-11390520.html',
        'uutiset-3-11586437.html', 'uutiset-3-11850913.html',
        'uutiset-3-7531710.html', 'uutiset-3-11881419.html',
        'uutiset-3-11498274.html', 'uutiset-3-10861434.html',
        'uutiset-3-11885787.html', 'uutiset-3-11141690.html',
        'uutiset-3-11991554.html', 'uutiset-3-11900100.html',
        'uutiset-3-10972951.html', 'uutiset-3-11463716.html',
        'uutiset-3-11710952.html', 'uutiset-3-11789546.html',
        'uutiset-3-11828730.html', 'uutiset-3-11260055.html',
        'uutiset-3-11852483.html', 'uutiset-3-11951384.html',
        'uutiset-3-11617491.html', 'uutiset-3-11379212.html',
        'uutiset-3-11289606.html', 'uutiset-3-5112171.html',
        'uutiset-3-10946709.html', 'uutiset-3-11566693.html',
        'uutiset-3-9216149.html']

        #sys.stdout.write(f"{counter}/{max_} processed")
        for source_file in test_sources:
            try:
                # Remove filepath related feature values.
                selector_vector = self.sources[source_file][self.num_of_non_selectors:]
                soup = None
                
                with open(f"{ self.source_file_dir }/{ source_file }", encoding="utf-8") as f:
                    soup = BeautifulSoup(f.read(), "lxml")

                
                for value, index in self.selectors:
                    # Does this file contain the considered selector?
                    if selector_vector[index]:
                        self.selector_to_content[value].append(to_lower_case(remove_extra_whitespace(self._dom_query_to_content(soup.find_all(class_=value)))))
            except Exception as e:
                print(f"Exception raised by { source_file }", e)

            counter += 1
            #sys.stdout.write("\r")
            #sys.stdout.write(f"{counter}/{max_} processed")
            
        #self._clean_content()
        self._sort_content()
        self._save_content()

    
    def calculate_entropies(self):
        self.extract_content()

        for selector in self.selector_to_content:
            if remove_extra_whitespace(self.selector_to_content[selector]) != "":
                content_bytes = self.selector_to_content[selector].encode("utf-8")
                self.selector_entropies[selector] = 8 * (len(zlib.compress(content_bytes)) - 20) / len(content_bytes)
                print(f"{ self.selector_entropies[selector] } { len(content_bytes) } { selector }")

            


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 4:
        classifier = CruncherClassifier(argv[1], argv[2], argv[3])
        classifier.calculate_entropies()
    else:
        raise ValueError("No paths given")
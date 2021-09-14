import io
import json
import os
import numpy as np
import sys
import hashlib

# Processes HTML files as streams and saves the result as a JSON file

class CruncherStreamer():
    # Read file stream and record all css selectors.
    def process_file(self, read_path):
        selectors = set()

        with open(read_path, encoding="utf-8") as f:
            debug = ""
            
            while True:
                try:
                    try:
                        c = f.read(1)
                    except UnicodeDecodeError:
                        # Probably an image file or other binary attachment.
                        continue

                    debug += c
                    # EOF detected.
                    if not c:
                        break

                    if c == "c":
                        pos = f.tell()

                        selector_test = self._parse_class_attribute(f)
                        debug += selector_test

                        if selector_test == "lass=":
                            try:
                                selector = self._parse_selector(f)
                                selectors.add(selector)
                                debug += selector
                            except ValueError as e:
                                continue
                        else:
                            f.seek(pos)

                except UnicodeDecodeError:
                    print(debug)
                    raise ValueError("test")
        
        return list(selectors)

    # Read return SOME_VALUE_HERE from "SOME_VALUE_HERE"
    def _parse_selector(self, stream):
        char = stream.read(1)
        if not char == "\"" and not char == "'":
            raise ValueError(f"Malformed class attribute { char }")

        selector = ""

        while True:
            char = stream.read(1)
            
            if not char:
                raise ValueError(f"Malformed class attribute { selector }")


            if char == '"' or char == "'":
                break

            selector += char

        return selector
    
    # c dectected. Attempt to read lass=.
    def _parse_class_attribute(self, stream):
        return stream.read(5)

        
    def save_result(self, path, bit_arrs, selector_mapping):
        print(f"Saving to { path }")
        with open(path, "w") as f:
            f.write(json.dumps({ "mapping": selector_mapping, "members": bit_arrs }))
            f.close()

    # Produce a vector of binary values indicating which selectors are in use.
    def _selectors_to_bits(self, selector_arr, selector_mapping):
        result = np.zeros(len(selector_mapping))

        result[[ selector_mapping[selector] for selector in selector_arr ]] += 1
        
        return list(result)

    # Produce mapping of filenames to selector bit vectors.
    def _produce_bit_vectors(self, file_selectors, selector_mapping):
        result = { }

        max_path_length = 0

        for filename in file_selectors:
            result[filename] = np.array([(int(hashlib.sha256(w.encode('utf-8')).hexdigest(), 16) % 10**3) / 10**i for i, w in enumerate(filename.split("-")[:-1])])
            max_path_length = max(max_path_length, len(result[filename]))

        for filename in file_selectors:
            path_name_features = np.zeros(max_path_length)
            path_name_features[:len(result[filename])] = result[filename]

            result[filename] = list(path_name_features) + self._selectors_to_bits(file_selectors[filename], selector_mapping)

        return result

    def process_arr(self, target_dir, write_dir):
        ## Process directory of files.
        selector_mapping = { }

        file_selectors = { }

        # Check that the inputs are valid directory paths
        if not self.is_directory(target_dir):
            raise ValueError("Target should be a directory of files!")

        if not self.is_directory(write_dir):
            if self.is_file(write_dir):
                raise ValueError("Write directory is a file!")
            self.create_directory(write_dir)

        max = len(os.listdir(target_dir))
        counter = 0
        
        for f in os.listdir(target_dir):
            sys.stdout.write("\r")
            sys.stdout.write(f"{counter}/{max} processed")

            selectors = self.process_file(os.path.join(target_dir, f))
            
            file_selectors[f] = selectors



            for selector in selectors:
                if selector not in selector_mapping:
                    selector_mapping[selector] = len(selector_mapping)
            counter += 1
            
        self.save_result(
            os.path.join(write_dir, "result.json"),
            self._produce_bit_vectors(file_selectors, selector_mapping),
            selector_mapping
            )

        


    # Check that the given path is a directory.
    def is_directory(self, path):
        return os.path.isdir(path)

    def is_file(self, path):
        return os.path.isfile(path)

    def create_directory(self, path):
        os.mkdir(path)

if __name__ == "__main__":
    from sys import argv

    cruncher = CruncherStreamer()

    if len(argv) == 3:
        cruncher.process_arr(argv[1], argv[2])
    else:
        raise ValueError("No paths given")
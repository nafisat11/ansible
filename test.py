from abc import ABC, abstractmethod
import re

class ModelSpec():                               # r3: HOR-E57-NN r4: HOR-R4E216GBR10G2
    def __init__(self, model, platform, family): #model, platform, family taken from /etc/3d-p/firmware
        self.create_model_spec = {}              #platform: r3. family: e57
        self.attributes = {"wifi80211Count": 0, "rajant24Count": 0,
                            "rajant50Count": 0, "lteCount": 0,
                            "meaCount": 0, "eth8023Count": 0,
                            "serial232Count": 0, "canCount": 0,
                            "c5915Count": 0, "c2020Count": 0}
        self._model = model
        self._platform = platform
        self._family = family

    @property
    def model(self):
        return self._model

    def add_attributes(self):
        if self._platform == "r3":
            radio_type = self._model.split("-")[2]
            if radio_type == "NN":
                print("2 x 802.11")


def main():
    m = ModelSpec("HOR-E57-NN", "r3", "e57")
    print(m.add_attributes())


if __name__ == '__main__':
    main()
from dbconnector import *
from item import *
import xml.dom.minidom


class Reactor(ShimstarItem):
    def __init__(self, id, idTemplate=0, new=False):
        super(Reactor, self).__init__(id, idTemplate)
        print "reactor::init " + str(id) + "/" + str(idTemplate)
        self.id = id
        self.label = ""
        self.templateId = idTemplate
        self.location = 0
        self.name = ""
        self.energy = 0
        self.cost = 0
        self.sell = 0
        self.energyCost = 0
        self.space = 0
        self.img = ""

        self.sound = ""
        self.typeItem = 0
        self.itemTemplateId = 0

        if new == False:
            if self.templateId == 0:
                self.loadFromBdd()
            else:
                self.loadFromTemplate()


    def getEnergy(self):
        return self.energy


    def loadFromTemplate(self):
        query = "SELECT star016_energy,star004_name, star004_energy, star004_mass,star004_space,star004_sell,star004_cost,star004_img,star004_type_star003,star004_id"
        # query+=""
        query += " FROM star004_item_template IT"
        query += " join star016_reactor w on w.star016_id = IT.star004_specific_starxxx "
        # ~ query+=" WHERE w.star017_id ='" + str(self.templateId) + "' and star004_id='" + str(self.id) + "'"
        query += " WHERE star004_id='" + str(self.templateId) + "'"
        print "reactor::loadFromTemplate " + query
        instanceDbConnector = shimDbConnector.getInstance()
        cursor = instanceDbConnector.getConnection().cursor()
        cursor.execute(query)
        result_set = cursor.fetchall()
        for row in result_set:
            self.name = row[1]
            self.energy = int(row[0])
            self.cost = int(row[6])
            self.sell = int(row[5])
            self.energyCost = int(row[2])
            self.space = int(row[4])
            self.img = row[7]
            self.typeItem = row[8]
            self.itemTemplateId = int(row[9])
        #~ self.templateId=int(row[10])
        # self.sound=str(row[10])
        #~ self.location=row[9]
        cursor.close()
        self.loadSkill()


    # ~ super(engine,self).loadFromTemplate()

    def loadFromBdd(self):
        query = "SELECT star016_energy, star004_name, star004_energy, star004_mass,star004_space,star004_sell,star004_cost,star004_img"
        query += ",star004_type_star003,star006_location,star004_id "
        query += " FROM star006_item I Join  star004_item_template IT on I.star006_template_star004=star004_id "
        query += " join star016_reactor w on w.star016_id = IT.star004_specific_starxxx "
        query += "WHERE I.star006_id = '" + str(self.id) + "'"
        instanceDbConnector = shimDbConnector.getInstance()
        cursor = instanceDbConnector.getConnection().cursor()
        print "reactor::loadFromBdd" + query
        cursor.execute(query)
        result_set = cursor.fetchall()
        for row in result_set:
            self.name = row[1]
            self.energy = int(row[0])
            self.cost = int(row[6])
            self.sell = int(row[5])
            self.energyCost = int(row[2])
            self.space = int(row[4])
            self.img = row[7]
            self.location = row[9]
            self.typeItem = row[8]
            self.itemTemplateId = int(row[10])
            self.templateId = int(row[10])
        cursor.close()
        self.loadSkill()


    def getSpecificXml(self, docXml, itemXml):
        energieXml = docXml.createElement("energy")
        energieXml.appendChild(docXml.createTextNode(str(self.energy)))

        itemXml.append(energieXml)


    def getXml(self, docXml=None):
        if docXml == None:
            docXml = xml.dom.minidom.Document()
        itemXml = docXml.createElement("item")
        nameXml = docXml.createElement("name")
        nameXml.appendChild(docXml.createTextNode(str(self.name)))
        tplXml = docXml.createElement("templateid")
        tplXml.appendChild(docXml.createTextNode(str(self.templateId)))
        typeitemXml = docXml.createElement("typeitem")
        typeitemXml.appendChild(docXml.createTextNode(str(self.typeItem)))
        energieXml = docXml.createElement("energy")
        energieXml.appendChild(docXml.createTextNode(str(self.energy)))

        costXml = docXml.createElement("cost")
        costXml.appendChild(docXml.createTextNode(str(self.cost)))
        sellXml = docXml.createElement("sell")
        sellXml.appendChild(docXml.createTextNode(str(self.sell)))
        energyXml = docXml.createElement("energyCost")
        energyXml.appendChild(docXml.createTextNode(str(self.energyCost)))
        spaceXml = docXml.createElement("space")
        spaceXml.appendChild(docXml.createTextNode(str(self.space)))
        imgXml = docXml.createElement("img")
        imgXml.appendChild(docXml.createTextNode(str(self.img)))
        locationXml = docXml.createElement("location")
        locationXml.appendChild(docXml.createTextNode(str(self.location)))
        soundXml = docXml.createElement("sound")
        soundXml.appendChild(docXml.createTextNode(str(self.sound)))

        itemXml.appendChild(nameXml)
        itemXml.appendChild(tplXml)
        itemXml.appendChild(typeitemXml)
        itemXml.appendChild(energieXml)
        itemXml.appendChild(sellXml)
        itemXml.appendChild(energyXml)
        itemXml.appendChild(spaceXml)
        itemXml.appendChild(imgXml)
        itemXml.appendChild(locationXml)
        itemXml.appendChild(costXml)
        itemXml.appendChild(soundXml)
        #~ print "engine::getXml" + itemXml.toxml()
        return itemXml


    @staticmethod
    def getListReactor():
        query = "SELECT STAR006_id FROM star006_item I Join  star004_item_template IT on I.star006_template_star004=star004_id"
        query += " WHERE star004_type_star003 = 3"
        instanceDbConnector = shimDbConnector.getInstance()
        cursor = instanceDbConnector.getConnection().cursor()
        cursor.execute(query)
        result_set = cursor.fetchall()
        result = []
        for row in result_set:
            result.append(int(row[0]))
        cursor.close()

        return result


    def saveToBDD(self):
        if self.templateId > 0:
            query = "update star004_item_template"
            query += " set star004_name='" + self.name + "', star004_img='" + self.img + "', star004_type_star003 ='" + str(
                self.typeItem) + "'"
            query += " WHERE star004_id='" + str(self.id) + "'"
            instanceDbConnector = shimDbConnector.getInstance()
            cursor = instanceDbConnector.getConnection().cursor()
            cursor.execute(query)
            cursor.close()

            query = "update star016_reactor"
            query += " set star016_energy = " + str(self.energy)
            query += " where star016_id = " + str(self.templateId)
            #~ print query
            instanceDbConnector = shimDbConnector.getInstance()
            cursor = instanceDbConnector.getConnection().cursor()
            cursor.execute(query)
            cursor.close()

            instanceDbConnector.commit()
        else:
            query = "insert into star016_reactor "
            query += " (star016_energy) values ('" + str(self.energy) + "')"
            instanceDbConnector = shimDbConnector.getInstance()
            cursor = instanceDbConnector.getConnection().cursor()
            cursor.execute(query)
            id = int(cursor.lastrowid)
            cursor.close()

            query = "insert into star004_item_template"
            query += " (star004_name,star004_img,star004_type_star003,star004_specific_starxxx) values"
            query += " ('" + str(self.name) + "','" + str(self.img) + "','" + str(self.typeItem) + "','" + str(id) + "')"
            #~ print query
            instanceDbConnector = shimDbConnector.getInstance()
            cursor = instanceDbConnector.getConnection().cursor()
            cursor.execute(query)
            cursor.close()

            instanceDbConnector.commit()


    def delete(self):
        #~ print "engine::delete"
        query = "delete from star004_item_template where star004_id = " + str(self.id)
        instanceDbConnector = shimDbConnector.getInstance()
        cursor = instanceDbConnector.getConnection().cursor()
        cursor.execute(query)
        cursor.close()

        query = "delete from star016_reactor where star016_id = " + str(self.templateId)
        instanceDbConnector = shimDbConnector.getInstance()
        cursor = instanceDbConnector.getConnection().cursor()
        cursor.execute(query)
        cursor.close()

        instanceDbConnector.commit()

	
	
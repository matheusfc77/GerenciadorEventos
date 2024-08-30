from ModelDAO.Event.IEventDAO import IEventDAO

class EventDAO(IEventDAO):

    def __init__(self, persist):
        self.persist = persist


    def getEventByName(self, event_name):
        conn = self.persist.getConnection()
        myquery = { "event_name": event_name }
        mydoc = conn.find(myquery)
        list_mydoc = [x for x in mydoc]
        return list_mydoc
    

    def getAllEvents(self, top=10):
        conn = self.persist.getConnection()
        mydoc = conn.find()
        list_mydoc = [x for x in mydoc][:top]
        return list_mydoc
    
    
    def insertEvents(self, events):
        conn = self.persist.getConnection()
        if not isinstance(events, list): events = [events]

        dict_events = [
            {'event_name': event.event_name, 'address': event.address, 'start_date': event.start_date, 'end_date': event.end_date}
            for event in events
        ]
        conn.insert_many(dict_events)


    def updateAddress(self, event_name, new_values):
        conn = self.persist.getConnection()
        myquery = { "event_name": event_name }
        newvalues = { "$set": new_values }
        conn.update_one(myquery, newvalues)

    
    def deleteEvent(self, event_name):
        conn = self.persist.getConnection()
        myquery = { "event_name": event_name }
        conn.delete_one(myquery)
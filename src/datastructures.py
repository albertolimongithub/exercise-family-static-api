
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        # example list of members
        self._members = []

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        new_id = self._next_id
        self._next_id += 1
        return new_id

    def add_member(self, member):
        # fill this method and update the return
        member["last_name"] = self.last_name
        member["id"] = self._generateId()
        member["lucky_numbers"] = list(member.get("lucky_numbers", set()))
        self._members.append(member)

        return member

    def delete_member(self, id):
        # fill this method and update the return
        for member in self._members:
            if member["id"] == id:
                self._members.remove(member)
                return True
            
        return False

    def update_member(self, id, updated_member):
        for index,member in enumerate(self._members): # to find an element AND its index in a list, we use method .enumerate(), which gets both the index and the element itself during each iteration
            if member["id"] == id:
                self._members[index] == updated_member
                return True
        return False

    def get_member(self, id):
        ## you have to implement this method
        ## loop all the members and return the one with the given id
        for member in self._members:
            if member["id"] == id:
                return member
        return None

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members

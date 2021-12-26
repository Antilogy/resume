export default class GroupsJS{
    /**Keeps track of all properties for a group */
    constructor(groupID = 0, paymentPerMember){
        this.groupID = groupID;
        this.paymentPerMember = paymentPerMember;
        this.groupSize = 0;
        this.items = []
    }
    /**Adds an item to the group */
    addItem(){
        this.items.push(0)
    }
    /**Removes an item from the group */
    removeItem(){
        this.items.pop()
    }

}
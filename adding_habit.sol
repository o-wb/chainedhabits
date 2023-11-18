// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HabitTracker {
    struct Habit {
        string name;
        address sender;
        uint256 deposit;
    }
    
    mapping(address => Habit[]) private habits;
    
    function addHabit(string memory _habitName) public payable {
        //require(msg.value > 0, "Please send some ether to create a habit.");
        require(msg.value > 1, "Please send more than 1 Wei.");
        
        Habit memory newHabit = Habit(_habitName, msg.sender, msg.value);
        habits[msg.sender].push(newHabit);
    }
    
    function getHabits() public view returns (Habit[] memory) {
        return habits[msg.sender];
    }
}

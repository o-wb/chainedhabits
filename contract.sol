// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HabitTracker {
    address private cartesiMachineAddress;
    mapping(address => string) private userDocuments;

    event DocumentUpdated(address indexed user, string documentHash);

    constructor(address _cartesiMachineAddress) {
        cartesiMachineAddress = _cartesiMachineAddress;
    }

    function updateDocument(string memory documentHash) external {
        require(msg.sender == cartesiMachineAddress, "Only the Cartesi VM can update the document");
        userDocuments[msg.sender] = documentHash;
        emit DocumentUpdated(msg.sender, documentHash);
    }

    function getDocument(address user) external view returns (string memory) {
        return userDocuments[user];
    }
}

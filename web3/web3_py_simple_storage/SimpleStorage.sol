// SPDX-License-Identifier: MIT

// another way to declare version: "pragma solidity ^0.6.0;"
pragma solidity >=0.6.0 <0.9.0;

// contract SimpleStorage{
//     uint256 favoriteNumber = 7; // cannot be negative number
//     int256 favoriteInt = -7;
//     bool favoriteBool = true;
//     string favoriteString = "hello world";
//     address favoriteAddress = 0x1C2bE776934c49c17aa4869b8d9408375F0194FE;
//     bytes32 favoriteByte = "Hello";
// }
contract SimpleStorage {
    uint256 favoriteNumber; // default value = 0

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    mapping(string => uint256) public nameToFavoriteNumber; // relates a data type with another different

    People[] public people;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    // view (functions to get value stored in blockchain - variable, structure or info stored). No gas cost as it does not change status
    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    // pure (functions to operate). No gas cost as it does not change status
    // function pureFunction(uint256 _number) public pure{
    //     _number + _number;
    // }

    // memory (it exists only while function is executed) - in this case variable is added to people array (list of people)
    // storage (variable remains after the function is executed)
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name)); // push is similar to append
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}

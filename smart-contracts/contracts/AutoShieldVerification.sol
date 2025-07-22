// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/Ownable.sol";

contract AutoShieldVerification is Ownable {

    constructor(address initialOwner) Ownable(initialOwner) {}

    enum VerificationStatus { UNVERIFIED, VERIFIED, SUSPECTED }

    struct Verification {
        VerificationStatus status;
        string attestationHash;
        uint256 lastChecked;
        uint256 confidenceScore;
    }

    uint256 private _verificationCounter;
    mapping(address => Verification) private _verifications;
    mapping(address => uint256[]) private _verificationTimestamps;
    mapping(address => uint8[]) private _verificationStatuses;
    mapping(address => uint256[]) private _verificationConfidenceScores;

    event VerificationUpdated(address indexed user, VerificationStatus status, string attestationHash);

    function getVerificationStatus(address user) external view returns (uint8, string memory, uint256, uint256) {
        Verification storage verification = _verifications[user];
        return (uint8(verification.status), verification.attestationHash, verification.lastChecked, verification.confidenceScore);
    }

    function updateVerification(address user, uint8 status, string calldata attestationHash, uint256 confidenceScore) external onlyOwner {
        require(status <= 2, "Invalid status");
        
        Verification storage verification = _verifications[user];
        verification.status = VerificationStatus(status);
        verification.attestationHash = attestationHash;
        verification.lastChecked = block.timestamp;
        verification.confidenceScore = confidenceScore;
        
        // Store history
        _verificationTimestamps[user].push(block.timestamp);
        _verificationStatuses[user].push(status);
        _verificationConfidenceScores[user].push(confidenceScore);
        
        _verificationCounter++;
        emit VerificationUpdated(user, VerificationStatus(status), attestationHash);
    }

    function getVerificationHistory(address user) external view returns (
        uint256[] memory timestamps,
        uint8[] memory statuses,
        uint256[] memory confidenceScores
    ) {
        return (
            _verificationTimestamps[user],
            _verificationStatuses[user],
            _verificationConfidenceScores[user]
        );
    }

    function getVerificationCount() external view returns (uint256) {
        return _verificationCounter;
    }
}

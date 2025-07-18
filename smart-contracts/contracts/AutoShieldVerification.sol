// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract AutoShieldVerification is Ownable {
    using Counters for Counters.Counter;

    enum VerificationStatus { UNVERIFIED, VERIFIED, SUSPECTED }

    struct Verification {
        VerificationStatus status;
        string attestationHash;
        uint256 lastChecked;
    }

    Counters.Counter private _verificationCounter;
    mapping(address => Verification) private _verifications;

    event VerificationUpdated(address indexed user, VerificationStatus status, string attestationHash);

    function getVerificationStatus(address user) external view returns (VerificationStatus, string memory, uint256) {
        Verification storage verification = _verifications[user];
        return (verification.status, verification.attestationHash, verification.lastChecked);
    }

    function updateVerification(address user, VerificationStatus status, string calldata attestationHash) external onlyOwner {
        Verification storage verification = _verifications[user];
        verification.status = status;
        verification.attestationHash = attestationHash;
        verification.lastChecked = block.timestamp;
        _verificationCounter.increment();
        emit VerificationUpdated(user, status, attestationHash);
    }

    function getVerificationCount() external view returns (uint256) {
        return _verificationCounter.current();
    }
}

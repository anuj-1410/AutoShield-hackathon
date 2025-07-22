const { ethers } = require("hardhat");

async function main() {
    console.log("🚀 Deploying to Blockdag Testnet...");
    console.log("================================");
    
    // Get the deployer account
    const [deployer] = await ethers.getSigners();
    console.log("📝 Deploying contracts with account:", deployer.address);
    
    // Check balance
    const balance = await deployer.provider.getBalance(deployer.address);
    console.log("💰 Account balance:", ethers.formatEther(balance), "BDAG");
    
    // Verify we're on the correct network
    const network = await ethers.provider.getNetwork();
    console.log("🌐 Network:", network.name);
    console.log("🔗 Chain ID:", network.chainId.toString());
    
    if (network.chainId !== 1043n) {
        console.warn("⚠️  Warning: Expected Chain ID 1043 for Blockdag testnet, got:", network.chainId.toString());
    }
    
    // Get the contract factory
    const AutoShield = await ethers.getContractFactory("AutoShieldVerification");
    
    // Deploy the contract with the deployer as the initial owner
    console.log("\n📦 Deploying AutoShieldVerification contract...");
    const contract = await AutoShield.deploy(deployer.address);
    
    // Wait for deployment to complete
    console.log("⏳ Waiting for deployment confirmation...");
    await contract.waitForDeployment();
    
    const contractAddress = await contract.getAddress();
    const deploymentTx = contract.deploymentTransaction();
    
    console.log("\n✅ Deployment Successful!");
    console.log("========================");
    console.log("📍 Contract Address:", contractAddress);
    console.log("🧾 Transaction Hash:", deploymentTx.hash);
    console.log("⛽ Gas Used:", deploymentTx.gasLimit.toString());
    
    // Display useful information
    console.log("\n📋 Deployment Summary");
    console.log("====================");
    console.log("Network: Blockdag Testnet");
    console.log("Contract: AutoShieldVerification");
    console.log("Address:", contractAddress);
    console.log("Explorer:", `https://explorer-testnet.blockdag.network/address/${contractAddress}`);
    
    // Save deployment info to file
    const fs = require('fs');
    const deploymentInfo = {
        network: "blockdag-testnet",
        contractName: "AutoShieldVerification",
        contractAddress: contractAddress,
        deployerAddress: deployer.address,
        transactionHash: deploymentTx.hash,
        blockNumber: deploymentTx.blockNumber,
        timestamp: new Date().toISOString(),
        explorerUrl: `https://explorer-testnet.blockdag.network/address/${contractAddress}`,
        chainId: network.chainId.toString(),
        gasUsed: deploymentTx.gasLimit.toString()
    };
    
    fs.writeFileSync(
        'blockdag-deployment.json', 
        JSON.stringify(deploymentInfo, null, 2)
    );
    
    console.log("\n💾 Deployment info saved to: blockdag-deployment.json");
    console.log("\n🎯 Next Steps:");
    console.log("1. Visit the explorer:", `https://explorer-testnet.blockdag.network/address/${contractAddress}`);
    console.log("2. Add the contract to your MetaMask using the address above");
    console.log("3. Verify the contract on the explorer if needed");
}

main()
    .then(() => {
        console.log("\n🎉 Deployment completed successfully!");
        process.exit(0);
    })
    .catch((error) => {
        console.error("\n❌ Deployment failed:");
        console.error(error);
        process.exit(1);
    });

"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"
import { useToast } from "@/hooks/use-toast"

// Web3 types
interface Web3ContextType {
  account: string | null
  isConnected: boolean
  isConnecting: boolean
  connect: () => Promise<void>
  disconnect: () => void
  network: string
  chainId: number | null
  balance: string | null
  provider: any
}

const Web3Context = createContext<Web3ContextType | undefined>(undefined)

// Ethereum provider interface
interface EthereumProvider {
  request: (args: { method: string; params?: any[] }) => Promise<any>
  on: (event: string, handler: (accounts: string[]) => void) => void
  removeListener: (event: string, handler: (accounts: string[]) => void) => void
  isMetaMask?: boolean
}

declare global {
  interface Window {
    ethereum?: EthereumProvider
  }
}

export function Web3Provider({ children }: { children: ReactNode }) {
  const [account, setAccount] = useState<string | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [isConnecting, setIsConnecting] = useState(false)
  const [network, setNetwork] = useState("Ethereum Mainnet")
  const { toast } = useToast()

  useEffect(() => {
    // Check if already connected on page load
    const savedAccount = localStorage.getItem("autoshield_account")
    if (savedAccount) {
      setAccount(savedAccount)
      setIsConnected(true)
    }
  }, [])

  const connect = async () => {
    setIsConnecting(true)

    try {
      // Simulate wallet connection
      await new Promise((resolve) => setTimeout(resolve, 1500))

      // Generate a mock wallet address
      const mockAddress = "0x" + Math.random().toString(16).substr(2, 40)

      setAccount(mockAddress)
      setIsConnected(true)
      localStorage.setItem("autoshield_account", mockAddress)

      toast({
        title: "Wallet Connected",
        description: `Connected to ${mockAddress.slice(0, 6)}...${mockAddress.slice(-4)}`,
      })
    } catch (error) {
      toast({
        title: "Connection Failed",
        description: "Failed to connect wallet. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsConnecting(false)
    }
  }

  const disconnect = () => {
    setAccount(null)
    setIsConnected(false)
    localStorage.removeItem("autoshield_account")

    toast({
      title: "Wallet Disconnected",
      description: "Your wallet has been disconnected.",
    })
  }

  return (
    <Web3Context.Provider
      value={{
        account,
        isConnected,
        isConnecting,
        connect,
        disconnect,
        network,
      }}
    >
      {children}
    </Web3Context.Provider>
  )
}

export function useWeb3() {
  const context = useContext(Web3Context)
  if (context === undefined) {
    throw new Error("useWeb3 must be used within a Web3Provider")
  }
  return context
}

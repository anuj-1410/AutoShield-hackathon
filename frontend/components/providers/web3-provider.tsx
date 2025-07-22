/**
 * @file Web3Provider component for AutoShield.
 * @description This provider manages the wallet connection state (real or sample),
 * handles connection/disconnection logic, and provides wallet info to the app.
 */

"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"
import { useToast } from "@/hooks/use-toast"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"

// --- Constants ---
// Define sample accounts for easy testing and demonstration.
const SAMPLE_ACCOUNTS = [
  { label: "Sample Verified Account", address: "0x1111111111111111111111111111111111111111", type: "verified" },
  { label: "Sample Suspected Fraud Account", address: "0x2222222222222222222222222222222222222222", type: "suspected" }
]

// --- Types ---
interface Web3ContextType {
  account: string | null
  isConnected: boolean
  isConnecting: boolean
  connect: () => void
  disconnect: () => void
  mockType: "real" | "verified" | "suspected" | null
}

interface EthereumProvider {
  request: (args: { method: string; params?: any[] }) => Promise<any>
}

declare global {
  interface Window {
    ethereum?: EthereumProvider
  }
}

const Web3Context = createContext<Web3ContextType | undefined>(undefined)

/**
 * Provides Web3 connection state and functions to its children.
 */
export function Web3Provider({ children }: { children: ReactNode }) {
  // --- State Management ---
  const [account, setAccount] = useState<string | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [isConnecting, setIsConnecting] = useState(false)
  const [mockType, setMockType] = useState<Web3ContextType['mockType']>(null)
  const [showConnectModal, setShowConnectModal] = useState(false)
  const { toast } = useToast()

  // --- Effects ---
  // On load, check localStorage to restore a previous session.
  useEffect(() => {
    const savedAccount = localStorage.getItem("autoshield_account")
    const savedType = localStorage.getItem("autoshield_account_type")
    if (savedAccount && savedType) {
      setAccount(savedAccount)
      setIsConnected(true)
      setMockType(savedType as Web3ContextType['mockType'])
    }
  }, [])

  // --- Connection Logic ---
  const connect = () => setShowConnectModal(true)

  const connectRealWallet = async () => {
    setIsConnecting(true)
    setShowConnectModal(false)
    try {
      if (!window.ethereum) {
        toast({ title: "MetaMask Not Detected", description: "Please install MetaMask to continue.", variant: "destructive" })
        window.open("https://metamask.io/download.html", "_blank")
        return
      }
      const [realAddress] = await window.ethereum.request({ method: "eth_requestAccounts" })
      handleConnection(realAddress, "real")
    } catch (error: any) {
      toast({ title: "Connection Failed", description: error?.message || "Could not connect wallet.", variant: "destructive" })
    } finally {
      setIsConnecting(false)
    }
  }

  const connectSampleWallet = (type: "verified" | "suspected") => {
    const sample = SAMPLE_ACCOUNTS.find(a => a.type === type)
    if (sample) {
      handleConnection(sample.address, type)
    }
    setShowConnectModal(false)
  }

  const handleConnection = (address: string, type: Web3ContextType['mockType']) => {
    setAccount(address)
    setIsConnected(true)
    setMockType(type)
    localStorage.setItem("autoshield_account", address)
    localStorage.setItem("autoshield_account_type", type || "")
    toast({ title: "Wallet Connected", description: `Connected to ${address.slice(0, 6)}...${address.slice(-4)}` })
  }

  const disconnect = () => {
    setAccount(null)
    setIsConnected(false)
    setMockType(null)
    localStorage.removeItem("autoshield_account")
    localStorage.removeItem("autoshield_account_type")
    toast({ title: "Wallet Disconnected" })
  }

  // --- Provider Value ---
  const value = { account, isConnected, isConnecting, connect, disconnect, mockType }

  return (
    <Web3Context.Provider value={value}>
      {children}
      <Dialog open={showConnectModal} onOpenChange={setShowConnectModal}>
        <DialogContent>
          <DialogHeader><DialogTitle>Connect Wallet</DialogTitle></DialogHeader>
          <div className="flex flex-col gap-4 py-4">
            <Button onClick={connectRealWallet} disabled={isConnecting}>Connect with MetaMask</Button>
            <Button onClick={() => connectSampleWallet("verified")} variant="outline">Use Sample Verified Account</Button>
            <Button onClick={() => connectSampleWallet("suspected")} variant="destructive">Use Sample Suspected Account</Button>
          </div>
        </DialogContent>
      </Dialog>
    </Web3Context.Provider>
  )
}

/**
 * Custom hook to easily access the Web3 context.
 */
export function useWeb3() {
  const context = useContext(Web3Context)
  if (context === undefined) {
    throw new Error("useWeb3 must be used within a Web3Provider")
  }
  return context
}

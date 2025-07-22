/**
 * @file DashboardPage component for AutoShield.
 * @description This is the main page for the user dashboard, displaying wallet verification status,
 * account information, and detailed analytics charts. It handles both real and sample wallet data.
 */

"use client"

import { useEffect, useState, useMemo } from "react"
import { Header } from "@/components/layout/header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { useWeb3 } from "@/components/providers/web3-provider"
import { Shield, Download, RefreshCw, AlertTriangle, CheckCircle, Clock, Loader2, CheckCircle2, BrainCircuit, BarChart3 } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { Line, Radar, Doughnut } from 'react-chartjs-2'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, RadialLinearScale, ArcElement, Tooltip, Legend } from 'chart.js'

// Register Chart.js components to be used.
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, RadialLinearScale, ArcElement, Tooltip, Legend)

/**
 * @interface VerificationStatus
 * @description Defines the structure for the verification data received from the backend.
 */
interface VerificationStatus {
  status: "verified" | "suspected" | "unverified"
  confidence: number
  lastChecked: string
  attestationHash?: string
  riskFactors: string[]
  accountCreationTimestamp?: number
  wallet_metrics?: {
    tx_timeline_labels?: string[]
    tx_timeline_incoming?: number[]
    tx_timeline_outgoing?: number[]
    wallet_age_days?: number
    tx_frequency_per_day?: number
    unique_counterparties?: number
    average_gas_fee_paid?: number
    contract_interaction_count?: number
    erc20_token_count?: number
    nft_count?: number
    risk_factor_contributions?: number[]
    tx_burstiness?: number
  }
}

/**
 * The main dashboard page component.
 */
export default function DashboardPage() {
  const { account, isConnected } = useWeb3()
  const { toast } = useToast()

  // --- State Management ---
  const [verificationStatus, setVerificationStatus] = useState<VerificationStatus | null>(null)
  const [loading, setLoading] = useState(false)
  const [progressStep, setProgressStep] = useState<null | "fetching" | "predicting" | "scoring" | "saving" | "done">(null)

  // --- Data Fetching ---
  // Fetch verification status when the wallet is connected.
  useEffect(() => {
    if (isConnected && account) {
      fetchVerificationStatus()
    }
  }, [isConnected, account])

  /**
   * Fetches the verification status from the backend API.
   */
  const fetchVerificationStatus = async () => {
    if (!account) return
    setLoading(true)
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/verification/status/${account}`)
      if (!response.ok) throw new Error('Failed to fetch verification status')
      
      const data = await response.json()
      // Transform backend response to the frontend's VerificationStatus interface.
      const transformedStatus: VerificationStatus = {
        status: data.status,
        confidence: data.confidence_score,
        lastChecked: data.analyzed_at,
        attestationHash: data.attestation_hash,
        riskFactors: data.risk_factors || [],
        accountCreationTimestamp: data.wallet_metrics?.account_creation_timestamp,
        wallet_metrics: data.wallet_metrics,
      }
      setVerificationStatus(transformedStatus)
    } catch (error) {
      console.error('Error fetching verification status:', error)
      toast({ title: "Error", description: "Failed to fetch verification status", variant: "destructive" })
    } finally {
      setLoading(false)
    }
  }

  // --- Actions ---
  /**
   * Initiates a re-verification request to the backend.
   * This shows a progress modal to the user.
   */
  const requestReVerification = async () => {
    if (!account) return
    setLoading(true)
    setProgressStep("fetching")
    try {
      // Simulate progress for better UX, then make the real backend call.
      await new Promise((res) => setTimeout(res, 800)); setProgressStep("predicting")
      await new Promise((res) => setTimeout(res, 1200)); setProgressStep("scoring")
      await new Promise((res) => setTimeout(res, 800)); setProgressStep("saving")
      await new Promise((res) => setTimeout(res, 1200))

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/verification/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ wallet_address: account, force_refresh: true })
      })
      if (!response.ok) throw new Error('Failed to request re-verification')
      
      setProgressStep("done")
      toast({ title: "Re-verification Completed", description: "Your account has been re-analyzed." })
      await fetchVerificationStatus()
      await new Promise((res) => setTimeout(res, 900))
    } catch (error) {
      console.error('Error requesting re-verification:', error)
      toast({ title: "Error", description: "Failed to request re-verification", variant: "destructive" })
    } finally {
      setLoading(false)
      setProgressStep(null)
    }
  }

  /**
   * Downloads the verification attestation as a JSON file.
   */
  const downloadAttestation = () => {
    if (!verificationStatus) return
    const attestationData = {
      address: account,
      status: verificationStatus.status,
      timestamp: verificationStatus.lastChecked,
      hash: verificationStatus.attestationHash,
    }
    const blob = new Blob([JSON.stringify(attestationData, null, 2)], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `autoshield-attestation-${account?.slice(0, 8)}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  // --- Memoized Chart Data ---
  // useMemo ensures that chart data is only recalculated when verificationStatus changes.
  const chartData = useMemo(() => {
    const metrics = verificationStatus?.wallet_metrics || {}
    return {
      line: {
        labels: metrics.tx_timeline_labels || [],
        datasets: [
          { label: "Incoming", data: metrics.tx_timeline_incoming || [], borderColor: "#22c55e", backgroundColor: "rgba(34,197,94,0.2)", tension: 0.4, fill: true },
          { label: "Outgoing", data: metrics.tx_timeline_outgoing || [], borderColor: "#3b82f6", backgroundColor: "rgba(59,130,246,0.2)", tension: 0.4, fill: true },
        ],
      },
      radar: {
        labels: ["Account Age", "Tx Diversity", "Counterparty Variety", "Gas Patterns", "Contract Interactions", "Asset Diversity"],
        datasets: [{
          label: "This Wallet",
          data: [
            Math.min((metrics.wallet_age_days || 0) / 365 * 100, 100),
            Math.min((metrics.tx_frequency_per_day || 0) * 10, 100),
            Math.min(metrics.unique_counterparties || 0, 100),
            Math.min((metrics.average_gas_fee_paid || 0) * 100, 100),
            Math.min(metrics.contract_interaction_count || 0, 100),
            Math.min((metrics.erc20_token_count || 0) + (metrics.nft_count || 0), 100),
          ],
          backgroundColor: "rgba(59,130,246,0.3)",
          borderColor: "#3b82f6",
          pointBackgroundColor: "#3b82f6",
        }],
      },
      doughnut: {
        labels: ["Account Maturity", "Tx Patterns", "Asset Diversity", "Social Signals", "Behavioral Consistency"],
        datasets: [{
          data: metrics.risk_factor_contributions || [metrics.wallet_age_days ? 30 : 0, metrics.tx_burstiness ? 25 : 0, (metrics.erc20_token_count || metrics.nft_count) ? 20 : 0, 0, 0],
          backgroundColor: ["#3b82f6", "#22c55e", "#f59e42", "#a855f7", "#f43f5e"],
          borderWidth: 2,
        }],
      },
    }
  }, [verificationStatus])

  // --- Render Logic ---
  // Show a prompt if the wallet is not connected.
  if (!isConnected) {
    return <ConnectWalletPrompt />
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Account Dashboard</h1>
          <p className="text-muted-foreground">Manage your verification status and download attestations.</p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-3 mb-6">
          <Button onClick={requestReVerification} disabled={loading} variant="default">
            <RefreshCw className="h-4 w-4 mr-2" /> Request Re-verification
          </Button>
          <Button onClick={downloadAttestation} disabled={!verificationStatus} variant="outline">
            <Download className="h-4 w-4 mr-2" /> Download Proof
          </Button>
        </div>

        {/* Main Content Grid */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <StatusCard loading={loading} status={verificationStatus} />
          <AccountInfoCard account={account} creationTimestamp={verificationStatus?.accountCreationTimestamp} />
        </div>

        {/* Charts Section */}
        <ChartsSection chartData={chartData} />

      </main>
      {progressStep && <ProgressModal step={progressStep} />}
    </div>
  )
}

// --- Sub-components for Cleaner Rendering ---

const ConnectWalletPrompt = () => (
  <div className="min-h-screen bg-background">
    <Header />
    <div className="container mx-auto px-4 py-16">
      <Card className="max-w-md mx-auto text-center">
        <CardHeader>
          <Shield className="h-12 w-12 mx-auto mb-4 text-primary" />
          <CardTitle>Connect Your Wallet</CardTitle>
          <CardDescription>Please connect your wallet to view your verification status.</CardDescription>
        </CardHeader>
      </Card>
    </div>
  </div>
)

const StatusCard = ({ loading, status }: { loading: boolean, status: VerificationStatus | null }) => {
  const getStatusIcon = (s: string) => {
    if (s === "verified") return <CheckCircle className="h-5 w-5 text-green-400" />
    if (s === "suspected") return <AlertTriangle className="h-5 w-5 text-red-400" />
    return <Clock className="h-5 w-5 text-yellow-400" />
  }
  const getStatusColor = (s: string) => `verification-${s}`

  return (
    <Card className="md:col-span-2">
      <CardHeader>
        <CardTitle className="flex items-center gap-2"><Shield className="h-5 w-5" />Verification Status</CardTitle>
        <CardDescription>Current verification status for your connected wallet.</CardDescription>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="space-y-4">
            <div className="h-4 bg-muted rounded animate-pulse w-full" />
            <div className="h-4 bg-muted rounded animate-pulse w-3/4" />
            <div className="h-4 bg-muted rounded animate-pulse w-1/2" />
          </div>
        ) : status ? (
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              {getStatusIcon(status.status)}
              <Badge className={getStatusColor(status.status)}>{status.status.toUpperCase()}</Badge>
              <span className="text-sm text-muted-foreground">{status.confidence}% confidence</span>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span>Verification Score</span>
                <span>{status.confidence}%</span>
              </div>
              <Progress value={status.confidence} className="h-2" />
            </div>
            <div className="text-sm text-muted-foreground">
              Last checked: {new Date(status.lastChecked).toLocaleString()}
            </div>
            {status.riskFactors.length > 0 && (
              <div>
                <h4 className="font-medium mb-2 text-red-400">Risk Factors:</h4>
                <ul className="text-sm space-y-1">
                  {status.riskFactors.map((factor, index) => (
                    <li key={index} className="flex items-center gap-2">
                      <AlertTriangle className="h-3 w-3 text-red-400" />
                      {factor}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ) : <p className="text-muted-foreground">No verification data available.</p>}
      </CardContent>
    </Card>
  )
}

const AccountInfoCard = ({ account, creationTimestamp }: { account: string | null, creationTimestamp?: number }) => (
  <Card>
    <CardHeader><CardTitle>Account Info</CardTitle></CardHeader>
    <CardContent className="space-y-4">
      <div>
        <div className="text-sm text-muted-foreground">Wallet Address</div>
        <div className="font-mono text-sm break-all">{account}</div>
      </div>
      <div>
        <div className="text-sm text-muted-foreground">Network</div>
        <div>Ethereum Mainnet</div>
      </div>
      <div>
        <div className="text-sm text-muted-foreground">Member Since</div>
        <div>{creationTimestamp ? new Date(creationTimestamp * 1000).toLocaleDateString() : "-"}</div>
      </div>
    </CardContent>
  </Card>
)

const ChartsSection = ({ chartData }: { chartData: any }) => (
  <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 mt-6">
    <Card>
      <CardHeader>
        <CardTitle>Transaction Activity</CardTitle>
        <CardDescription>Daily incoming vs. outgoing transactions.</CardDescription>
      </CardHeader>
      <CardContent>
        <Line data={chartData.line} options={{ responsive: true, plugins: { legend: { display: true } }, elements: { point: { radius: 2 } } }} height={180} />
      </CardContent>
    </Card>
    <Card>
      <CardHeader>
        <CardTitle>Wallet Behavior</CardTitle>
        <CardDescription>Multi-axis behavioral profile.</CardDescription>
      </CardHeader>
      <CardContent>
        <Radar data={chartData.radar} options={{ responsive: true, plugins: { legend: { display: false } } }} height={180} />
      </CardContent>
    </Card>
    <Card>
      <CardHeader>
        <CardTitle>Risk Breakdown</CardTitle>
        <CardDescription>Factors influencing your score.</CardDescription>
      </CardHeader>
      <CardContent>
        <Doughnut data={chartData.doughnut} options={{ responsive: true, plugins: { legend: { display: true, position: "bottom" } }, cutout: "70%" }} height={180} />
      </CardContent>
    </Card>
  </div>
)

const ProgressModal = ({ step }: { step: string }) => {
  const steps = [
    { key: "fetching", label: "Fetching Wallet Data", icon: <Loader2 className={step === "fetching" ? "animate-spin text-blue-500" : ""} /> },
    { key: "predicting", label: "AI Prediction", icon: <BrainCircuit className={step === "predicting" ? "animate-pulse text-purple-500" : ""} /> },
    { key: "scoring", label: "Scoring & Risk Analysis", icon: <BarChart3 className={step === "scoring" ? "animate-pulse text-green-500" : ""} /> },
    { key: "saving", label: "Saving to Contract", icon: <Shield className={step === "saving" ? "animate-pulse text-orange-500" : ""} /> },
    { key: "done", label: "Completed", icon: <CheckCircle2 className={step === "done" ? "text-emerald-500" : ""} /> },
  ]
  const currentStepIndex = steps.findIndex(s => s.key === step)

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="bg-background rounded-xl shadow-xl p-8 min-w-[320px] flex flex-col items-center gap-6 border">
        <h3 className="text-lg font-semibold">Re-verification In Progress</h3>
        <div className="flex flex-col gap-4 w-full">
          {steps.map((s, i) => (
            <div key={s.key} className={`flex items-center gap-3 py-1 ${i <= currentStepIndex ? "font-semibold" : "opacity-50"}`}>
              <span className="h-6 w-6 flex items-center justify-center">{s.icon}</span>
              <span>{s.label}</span>
              {i < currentStepIndex && <CheckCircle2 className="h-5 w-5 text-emerald-400 ml-auto" />}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

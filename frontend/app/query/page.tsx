"use client"

import { useState } from "react"
import { Header } from "@/components/layout/header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Search, AlertTriangle, CheckCircle, Clock } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

interface QueryResult {
  address: string
  status: "verified" | "suspected" | "unverified"
  confidence: number
  lastChecked: string
  attestationHash?: string
  blockchainTxHash?: string
  riskFactors: string[]
  publicInfo?: {
    transactionCount: number
    accountAge: string
    riskScore: number
    walletAgeDays: number
    uniqueCounterparties: number
    avgGasFee: number
  }
}

export default function QueryPage() {
  const [searchAddress, setSearchAddress] = useState("")
  const [queryResult, setQueryResult] = useState<QueryResult | null>(null)
  const [loading, setLoading] = useState(false)
  const { toast } = useToast()

  const handleQuery = async () => {
    if (!searchAddress.trim()) {
      toast({
        title: "Invalid Address",
        description: "Please enter a valid wallet address",
        variant: "destructive",
      })
      return
    }

    // Basic validation
    if (!searchAddress.startsWith('0x') || searchAddress.length !== 42) {
      toast({
        title: "Invalid Address",
        description: "Please enter a valid Ethereum address",
        variant: "destructive",
      })
      return
    }

    setLoading(true)

    try {
      // Call backend API
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/verification/status/${searchAddress}`)
      if (!response.ok) {
        throw new Error('Failed to fetch verification status')
      }
      
      const data = await response.json()
      
      // Transform backend response
      const metrics = data.wallet_metrics || {}
      const result: QueryResult = {
        address: searchAddress,
        status: data.status,
        confidence: data.confidence_score,
        lastChecked: data.analyzed_at,
        attestationHash: data.attestation_hash,
        blockchainTxHash: data.blockchain_tx_hash,
        riskFactors: data.risk_factors || [],
        publicInfo: {
          transactionCount: metrics.tx_count || 0,
          accountAge: metrics.wallet_age_days ? `${Math.floor(metrics.wallet_age_days / 30)} months` : "Unknown",
          riskScore: data.risk_score || 0,
          walletAgeDays: metrics.wallet_age_days || 0,
          uniqueCounterparties: metrics.unique_counterparties || 0,
          avgGasFee: metrics.average_gas_fee_paid || 0,
        },
      }
      
      setQueryResult(result)
    } catch (error) {
      console.error('Error querying address:', error)
      toast({
        title: "Error",
        description: "Failed to query address verification status",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "verified":
        return <CheckCircle className="h-5 w-5 text-green-400" />
      case "suspected":
        return <AlertTriangle className="h-5 w-5 text-red-400" />
      default:
        return <Clock className="h-5 w-5 text-yellow-400" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "verified":
        return "verification-verified"
      case "suspected":
        return "verification-suspected"
      default:
        return "verification-unverified"
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Public Query Tool</h1>
          <p className="text-muted-foreground">
            Check the verification status of any wallet address on the AutoShield network
          </p>
        </div>

        <Card className="max-w-2xl mx-auto">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Search className="h-5 w-5" />
              Address Verification Lookup
            </CardTitle>
            <CardDescription>Enter a wallet address to check its verification status</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex gap-2">
                <Input
                  placeholder="0x742d35Cc6634C0532925a3b8D4C9db96590c6C87"
                  value={searchAddress}
                  onChange={(e) => setSearchAddress(e.target.value)}
                  className="font-mono"
                />
                <Button onClick={handleQuery} disabled={loading}>
                  {loading ? "Searching..." : "Query"}
                </Button>
              </div>

              {queryResult && (
                <div className="mt-6 space-y-4">
                  <div className="border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="font-semibold">Verification Result</h3>
                      <div className="flex items-center gap-2">
                        {getStatusIcon(queryResult.status)}
                        <Badge className={getStatusColor(queryResult.status)}>{queryResult.status.toUpperCase()}</Badge>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <div>
                        <div className="text-sm text-muted-foreground">Address</div>
                        <div className="font-mono text-sm break-all">{queryResult.address}</div>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <div className="text-sm text-muted-foreground">Confidence Score</div>
                          <div className="text-lg font-semibold">{queryResult.confidence}%</div>
                        </div>
                        <div>
                          <div className="text-sm text-muted-foreground">Last Checked</div>
                          <div className="text-sm">{new Date(queryResult.lastChecked).toLocaleString()}</div>
                        </div>
                      </div>

                      {queryResult.publicInfo && (
                        <div className="border-t pt-4">
                          <h4 className="font-medium mb-3">Wallet Metrics</h4>
                          <div className="grid grid-cols-3 gap-4 text-sm">
                            <div>
                              <div className="text-muted-foreground">Transactions</div>
                              <div className="font-medium">{queryResult.publicInfo.transactionCount}</div>
                            </div>
                            <div>
                              <div className="text-muted-foreground">Account Age</div>
                              <div className="font-medium">{queryResult.publicInfo.accountAge}</div>
                            </div>
                            <div>
                              <div className="text-muted-foreground">Risk Score</div>
                              <div className="font-medium">{queryResult.publicInfo.riskScore}/100</div>
                            </div>
                            <div>
                              <div className="text-muted-foreground">Counterparties</div>
                              <div className="font-medium">{queryResult.publicInfo.uniqueCounterparties}</div>
                            </div>
                            <div>
                              <div className="text-muted-foreground">Avg Gas Fee</div>
                              <div className="font-medium">{(queryResult.publicInfo.avgGasFee * 1e9).toFixed(2)} Gwei</div>
                            </div>
                            <div>
                              <div className="text-muted-foreground">Wallet Age</div>
                              <div className="font-medium">{queryResult.publicInfo.walletAgeDays} days</div>
                            </div>
                          </div>
                        </div>
                      )}
                      
                      {queryResult.riskFactors.length > 0 && (
                        <div className="border-t pt-4">
                          <h4 className="font-medium mb-3 text-red-400">Risk Factors</h4>
                          <ul className="text-sm space-y-1">
                            {queryResult.riskFactors.map((factor, index) => (
                              <li key={index} className="flex items-center gap-2">
                                <AlertTriangle className="h-3 w-3 text-red-400" />
                                {factor}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      {(queryResult.attestationHash || queryResult.blockchainTxHash) && (
                        <div className="border-t pt-4">
                          <h4 className="font-medium mb-3">Blockchain Info</h4>
                          <div className="space-y-2 text-sm">
                            {queryResult.attestationHash && (
                              <div>
                                <div className="text-muted-foreground">Attestation Hash</div>
                                <div className="font-mono text-xs break-all">{queryResult.attestationHash}</div>
                              </div>
                            )}
                            {queryResult.blockchainTxHash && (
                              <div>
                                <div className="text-muted-foreground">Transaction Hash</div>
                                <div className="font-mono text-xs break-all">{queryResult.blockchainTxHash}</div>
                              </div>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="text-xs text-muted-foreground">
                    This information is publicly available on the blockchain and updated in real-time. For privacy
                    reasons, detailed analysis results are not shown.
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* API Documentation */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Developer Integration</CardTitle>
            <CardDescription>Integrate AutoShield verification into your dApp</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h4 className="font-medium mb-2">Smart Contract Query</h4>
                <div className="bg-muted p-3 rounded font-mono text-sm">
                  {`contract.getVerificationStatus("0x742d35Cc...")`}
                </div>
              </div>
              <div>
                <h4 className="font-medium mb-2">REST API Endpoint</h4>
                <div className="bg-muted p-3 rounded font-mono text-sm">{`GET /api/v1/verification/status/0x742d35Cc...`}</div>
              </div>
              <Button variant="outline" className="w-full bg-transparent">
                View Full API Documentation
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

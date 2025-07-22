/**
 * API service for AutoShield frontend
 * Handles communication with backend services
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export interface VerificationRequest {
  wallet_address: string
  force_refresh?: boolean
}

export interface VerificationResponse {
  wallet_address: string
  status: 'verified' | 'suspected' | 'unverified'
  confidence_score: number
  risk_score?: number
  risk_factors: string[]
  attestation_hash?: string
  blockchain_tx_hash?: string
  model_version: string
  analyzed_at: string
  processing_time_ms?: number
}

export interface SystemStats {
  total_verifications: number
  verified_accounts: number
  suspected_accounts: number
  unverified_accounts: number
  accuracy_rate: number
  false_positive_rate: number
  avg_processing_time: number
  system_health: number
}

export interface FlaggedAccount {
  wallet_address: string
  risk_score: number
  flagged_at: string
  reasons: string[]
  status: 'pending' | 'reviewed' | 'confirmed' | 'dismissed'
}

class ApiService {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`
    
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    })

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`)
    }

    return response.json()
  }

  // Verification endpoints
  async analyzeAccount(request: VerificationRequest): Promise<VerificationResponse> {
    return this.request<VerificationResponse>('/verification/analyze', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }

  async getVerificationStatus(walletAddress: string): Promise<VerificationResponse> {
    return this.request<VerificationResponse>(`/verification/status/${walletAddress}`)
  }

  async reAnalyzeAccount(request: VerificationRequest): Promise<VerificationResponse> {
    return this.request<VerificationResponse>('/verification/re-analyze', {
      method: 'POST',
      body: JSON.stringify({ ...request, force_refresh: true }),
    })
  }

  async getVerificationHistory(walletAddress: string, limit: number = 10) {
    return this.request(`/verification/history/${walletAddress}?limit=${limit}`)
  }

  async batchAnalyze(walletAddresses: string[]): Promise<VerificationResponse[]> {
    return this.request<VerificationResponse[]>('/verification/batch-analyze', {
      method: 'POST',
      body: JSON.stringify({ wallet_addresses: walletAddresses }),
    })
  }

  // Analytics endpoints
  async getSystemStats(): Promise<SystemStats> {
    return this.request<SystemStats>('/analytics/system-stats')
  }

  async getDailyStats(days: number = 7) {
    return this.request(`/analytics/daily-stats?days=${days}`)
  }

  // Admin endpoints
  async getFlaggedAccounts(status?: string, limit: number = 50) {
    const params = new URLSearchParams()
    if (status) params.append('status', status)
    params.append('limit', limit.toString())
    
    return this.request(`/admin/flagged-accounts?${params}`)
  }

  async reviewFlaggedAccount(walletAddress: string, action: 'confirm' | 'dismiss', notes?: string) {
    return this.request(`/admin/flagged-accounts/${walletAddress}/review`, {
      method: 'POST',
      body: JSON.stringify({ action, notes }),
    })
  }

  // Blockchain endpoints
  async getNetworkInfo() {
    return this.request('/blockchain/network-info')
  }

  async getTransaction(txHash: string) {
    return this.request(`/blockchain/transaction/${txHash}`)
  }

  async estimateGas(walletAddress: string, status: string, attestationHash: string) {
    const params = new URLSearchParams({
      wallet_address: walletAddress,
      status,
      attestation_hash: attestationHash,
    })
    
    return this.request(`/blockchain/gas-estimate?${params}`)
  }
}

export const apiService = new ApiService()
export default apiService

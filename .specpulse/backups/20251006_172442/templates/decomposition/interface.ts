/**
 * {{service_name}} Service Interfaces
 * Generated from SPEC-{{spec_id}}
 */

// ============================================================================
// Domain Entities
// ============================================================================

export interface {{Entity}} {
  id: string;
  name: string;
  description?: string;
  status: {{Entity}}Status;
  metadata?: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
}

export enum {{Entity}}Status {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  PENDING = 'pending',
  DELETED = 'deleted'
}

// ============================================================================
// Request/Response DTOs
// ============================================================================

export interface Create{{Entity}}Request {
  name: string;
  description?: string;
  metadata?: Record<string, any>;
}

export interface Update{{Entity}}Request {
  name?: string;
  description?: string;
  status?: {{Entity}}Status;
  metadata?: Record<string, any>;
}

export interface {{Entity}}Response {
  data: {{Entity}};
  meta?: ResponseMeta;
}

export interface {{Entity}}ListResponse {
  data: {{Entity}}[];
  meta: PaginationMeta;
}

// ============================================================================
// Service Interface
// ============================================================================

export interface {{ServiceName}}Service {
  // CRUD Operations
  create(data: Create{{Entity}}Request): Promise<{{Entity}}>;
  findById(id: string): Promise<{{Entity}} | null>;
  findAll(params: QueryParams): Promise<{{Entity}}ListResponse>;
  update(id: string, data: Update{{Entity}}Request): Promise<{{Entity}}>;
  delete(id: string): Promise<boolean>;

  // Business Operations
  activate(id: string): Promise<{{Entity}}>;
  deactivate(id: string): Promise<{{Entity}}>;
  bulkUpdate(ids: string[], data: Update{{Entity}}Request): Promise<{{Entity}}[]>;

  // Query Operations
  findByName(name: string): Promise<{{Entity}} | null>;
  findByStatus(status: {{Entity}}Status): Promise<{{Entity}}[]>;
  search(query: SearchQuery): Promise<{{Entity}}[]>;
}

// ============================================================================
// Repository Interface
// ============================================================================

export interface {{Entity}}Repository {
  // Basic CRUD
  save(entity: {{Entity}}): Promise<{{Entity}}>;
  findById(id: string): Promise<{{Entity}} | null>;
  findAll(options?: FindOptions): Promise<{{Entity}}[]>;
  update(id: string, data: Partial<{{Entity}}>): Promise<{{Entity}} | null>;
  delete(id: string): Promise<boolean>;

  // Batch Operations
  saveMany(entities: {{Entity}}[]): Promise<{{Entity}}[]>;
  deleteMany(ids: string[]): Promise<number>;

  // Query Methods
  findOne(filter: FilterQuery): Promise<{{Entity}} | null>;
  find(filter: FilterQuery, options?: FindOptions): Promise<{{Entity}}[]>;
  count(filter?: FilterQuery): Promise<number>;
  exists(filter: FilterQuery): Promise<boolean>;
}

// ============================================================================
// Event Interfaces
// ============================================================================

export interface {{Entity}}Event {
  eventId: string;
  eventType: {{Entity}}EventType;
  entityId: string;
  timestamp: Date;
  data: {{Entity}};
  metadata?: EventMetadata;
}

export enum {{Entity}}EventType {
  CREATED = '{{entity}}.created',
  UPDATED = '{{entity}}.updated',
  DELETED = '{{entity}}.deleted',
  ACTIVATED = '{{entity}}.activated',
  DEACTIVATED = '{{entity}}.deactivated'
}

export interface EventMetadata {
  userId?: string;
  correlationId?: string;
  source?: string;
  version?: string;
}

// ============================================================================
// Error Interfaces
// ============================================================================

export class {{Entity}}Error extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number,
    public details?: any
  ) {
    super(message);
    this.name = '{{Entity}}Error';
  }
}

export class {{Entity}}NotFoundError extends {{Entity}}Error {
  constructor(id: string) {
    super(
      `{{Entity}} with ID ${id} not found`,
      'ENTITY_NOT_FOUND',
      404
    );
  }
}

export class {{Entity}}ValidationError extends {{Entity}}Error {
  constructor(message: string, details: any) {
    super(message, 'VALIDATION_ERROR', 400, details);
  }
}

// ============================================================================
// Helper Types
// ============================================================================

export interface QueryParams {
  page?: number;
  limit?: number;
  sort?: SortField;
  order?: SortOrder;
  filter?: FilterQuery;
}

export interface FilterQuery {
  [field: string]: any;
}

export interface FindOptions {
  skip?: number;
  limit?: number;
  sort?: SortOptions;
  projection?: ProjectionOptions;
}

export interface SortOptions {
  [field: string]: SortOrder;
}

export interface ProjectionOptions {
  [field: string]: 0 | 1;
}

export type SortField = 'name' | 'status' | 'createdAt' | 'updatedAt';
export type SortOrder = 'asc' | 'desc' | 1 | -1;

export interface PaginationMeta {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
  hasNext: boolean;
  hasPrev: boolean;
}

export interface ResponseMeta {
  timestamp: Date;
  version: string;
  [key: string]: any;
}

export interface SearchQuery {
  text?: string;
  fields?: string[];
  fuzzy?: boolean;
  limit?: number;
}

// ============================================================================
// Configuration Interface
// ============================================================================

export interface {{ServiceName}}Config {
  serviceName: string;
  port: number;
  database: DatabaseConfig;
  cache?: CacheConfig;
  messaging?: MessagingConfig;
  monitoring?: MonitoringConfig;
}

export interface DatabaseConfig {
  url: string;
  poolSize?: number;
  timeout?: number;
}

export interface CacheConfig {
  url: string;
  ttl?: number;
  prefix?: string;
}

export interface MessagingConfig {
  url: string;
  exchange?: string;
  queue?: string;
}

export interface MonitoringConfig {
  enabled: boolean;
  endpoint?: string;
  interval?: number;
}
// Interface for {{service_name}}

export interface {{InterfaceName}} {
  id: string;
  createdAt: Date;
  updatedAt: Date;
  // Add fields
}

export interface {{ServiceName}}Service {
  create(data: Partial<{{InterfaceName}}>): Promise<{{InterfaceName}}>;
  findById(id: string): Promise<{{InterfaceName}} | null>;
  update(id: string, data: Partial<{{InterfaceName}}>): Promise<{{InterfaceName}}>;
  delete(id: string): Promise<boolean>;
}

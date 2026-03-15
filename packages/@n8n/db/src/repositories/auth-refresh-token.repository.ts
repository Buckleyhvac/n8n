import { Service } from '@n8n/di';
import { DataSource, Repository } from '@n8n/typeorm';

import { AuthRefreshToken } from '../entities';

@Service()
export class AuthRefreshTokenRepository extends Repository<AuthRefreshToken> {
	constructor(dataSource: DataSource) {
		super(AuthRefreshToken, dataSource.manager);
	}
}

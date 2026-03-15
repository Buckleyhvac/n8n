import { Column, Entity, Index, PrimaryColumn } from '@n8n/typeorm';

import { DateTimeColumn } from './abstract-entity';

@Entity()
export class AuthRefreshToken {
	@PrimaryColumn()
	tokenHash: string;

	@Index()
	@Column()
	userId: string;

	@Column({ nullable: true })
	browserIdHash: string | null;

	@Column()
	userHash: string;

	@Column()
	usedMfa: boolean;

	@DateTimeColumn()
	expiresAt: Date;
}

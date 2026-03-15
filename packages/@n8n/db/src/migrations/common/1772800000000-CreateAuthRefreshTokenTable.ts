import type { MigrationContext, ReversibleMigration } from '../migration-types';

const tableName = 'auth_refresh_token';

export class CreateAuthRefreshTokenTable1772800000000 implements ReversibleMigration {
	async up({ schemaBuilder: { createTable, column, index } }: MigrationContext) {
		await createTable(tableName).withColumns(
			column('tokenHash').varchar(64).primary,
			column('userId').uuid.notNull,
			column('browserIdHash').varchar(255),
			column('userHash').varchar(64).notNull,
			column('usedMfa').bool.notNull,
			column('expiresAt').timestamp().notNull,
		);

		await index(tableName, ['userId']);
	}

	async down({ schemaBuilder: { dropTable } }: MigrationContext) {
		await dropTable(tableName);
	}
}

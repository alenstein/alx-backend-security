import ipaddress
from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP


class Command(BaseCommand):
    help = 'Adds one or more IP addresses to the blocklist.'

    def add_arguments(self, parser):
        parser.add_argument('ips', nargs='+', type=str, help='The IP address(es) to block.')

    def handle(self, *args, **options):
        ips_to_block = options['ips']
        for ip_str in ips_to_block:
            try:
                # Validate that the input is a valid IP address
                ipaddress.ip_address(ip_str)

                # Create or get the BlockedIP object
                obj, created = BlockedIP.objects.get_or_create(ip_address=ip_str)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully blocked IP: {ip_str}'))
                else:
                    self.stdout.write(self.style.WARNING(f'IP {ip_str} was already blocked.'))
            except ValueError:
                raise CommandError(f'"{ip_str}" is not a valid IP address.')
            except Exception as e:
                raise CommandError(f'An error occurred while blocking {ip_str}: {e}')
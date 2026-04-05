/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_hex.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/14 15:38:11 by tsellak           #+#    #+#             */
/*   Updated: 2025/11/14 15:38:12 by tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_print_hex(unsigned int n, const char format)
{
	int	len;

	len = 0;
	if (n >= 16)
		len += ft_print_hex(n / 16, format);
	if (format == 'x')
		len += ft_print_char("0123456789abcdef"[n % 16]);
	else if (format == 'X')
		len += ft_print_char("0123456789ABCDEF"[n % 16]);
	return (len);
}

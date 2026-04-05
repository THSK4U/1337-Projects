/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_ptr.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/14 15:38:09 by tsellak           #+#    #+#             */
/*   Updated: 2025/11/15 16:00:19 by tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	ft_print_long(unsigned long long n)
{
	int	len;

	len = 0;
	if (n >= 16)
		len += ft_print_long(n / 16);
	len += ft_print_char("0123456789abcdef"[n % 16]);
	return (len);
}

int	ft_print_ptr(unsigned long long ptr)
{
	int	len;

	len = 0;
	if (ptr == 0)
		return (ft_print_str("(nil)"));
	else
	{
		len += ft_print_str("0x");
		len += ft_print_long(ptr);
	}
	return (len);
}
